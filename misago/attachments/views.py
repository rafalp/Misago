from typing import Protocol, cast

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.module_loading import import_string
from django.utils.translation import pgettext
from django.views import View
from django.urls import reverse

from ..permissions.attachments import (
    check_delete_attachment_permission,
    check_download_attachment_permission,
)
from ..permissions.checkutils import check_permissions
from ..permissions.enums import CanUploadAttachments
from ..permissions.posts import check_see_post_permission
from .enums import AllowedAttachments
from .hooks import get_attachment_details_page_context_data_hook
from .models import Attachment
from .upload import handle_attachments_upload


class ServerProtocol(Protocol):
    def __call__(
        request: HttpRequest, attachment: Attachment, thumbnail: bool = False
    ) -> HttpResponse: ...


server = cast(ServerProtocol, import_string(settings.MISAGO_ATTACHMENTS_SERVER))


class AttachmentView(View):
    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        attachment = self.get_attachment(request, id, slug)
        return self.create_response(request, attachment)

    def get_attachment(self, request: HttpRequest, id: int, slug: str) -> Attachment:
        attachment = get_object_or_404(Attachment.objects.select_related(), id=id)

        if attachment.slug != slug:
            raise Http404()

        # Check attachment permissions if its not viewed by admin
        if not (request.user.is_authenticated and request.user.is_misago_admin):
            if attachment.is_deleted:
                raise Http404()

            check_download_attachment_permission(
                request.user_permissions,
                attachment.category,
                attachment.thread,
                attachment.post,
                attachment,
            )

        return attachment

    def create_response(
        self, request: HttpRequest, attachment: Attachment
    ) -> HttpResponse:
        raise NotImplementedError(
            "Views extending 'AttachmentView' must "
            "implement the 'create_response' method"
        )


class AttachmentDownloadView(AttachmentView):
    def create_response(
        self, request: HttpRequest, attachment: Attachment
    ) -> HttpResponse:
        if not attachment.upload:
            raise Http404()

        return server(request, attachment)


class AttachmentThumbnailView(AttachmentView):
    def create_response(
        self, request: HttpRequest, attachment: Attachment
    ) -> HttpResponse:
        if not attachment.thumbnail:
            raise Http404()

        return server(request, attachment, thumbnail=True)


class AttachmentDetailsView(AttachmentView):
    template_name: str = "misago/attachment_details/index.html"

    def create_response(
        self, request: HttpRequest, attachment: Attachment
    ) -> HttpResponse:
        if not attachment.upload:
            raise Http404()

        return render(
            self.request,
            self.template_name,
            self.get_context_data(request, attachment),
        )

    def get_context_data(self, request: HttpRequest, attachment: Attachment) -> dict:
        return get_attachment_details_page_context_data_hook(
            self.get_context_data_action, request, attachment
        )

    def get_context_data_action(
        self, request: HttpRequest, attachment: Attachment
    ) -> dict:
        with check_permissions() as can_see_post:
            check_see_post_permission(
                request.user_permissions,
                attachment.category,
                attachment.thread,
                attachment.post,
            )

        with check_permissions() as can_delete:
            check_delete_attachment_permission(
                request.user_permissions,
                attachment.category,
                attachment.thread,
                attachment.post,
                attachment,
            )

        return {
            "attachment": attachment,
            "can_delete_attachment": can_delete,
            "can_see_post": can_see_post,
            "attachment_referer": _get_referer_querystring(request, attachment),
        }


class AttachmentDeleteView(View):
    template_name: str = "misago/attachment_delete/index.html"

    def get(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        attachment = self.get_attachment(request, id, slug)

        return render(
            request,
            self.template_name,
            {
                "attachment": attachment,
                "attachment_referer": _get_referer_querystring(request, attachment),
            },
        )

    def post(self, request: HttpRequest, id: int, slug: str) -> HttpResponse:
        attachment = self.get_attachment(request, id, slug)
        attachment.delete()

        messages.success(
            request,
            pgettext("attachment delete page", 'Attachment "%(name)s" deleted')
            % {"name": attachment.name},
        )

        return redirect(self.get_redirect_url(request, attachment))

    def get_attachment(self, request: HttpRequest, id: int, slug: str) -> Attachment:
        attachment = get_object_or_404(Attachment.objects.select_related(), id=id)

        if attachment.slug != slug:
            raise Http404()

        # Check attachment permissions if its not viewed by admin
        if not (request.user.is_authenticated and request.user.is_misago_admin):
            if attachment.is_deleted:
                raise Http404()

        check_delete_attachment_permission(
            request.user_permissions,
            attachment.category,
            attachment.thread,
            attachment.post,
            attachment,
        )

        return attachment

    def get_redirect_url(self, request: HttpRequest, attachment: Attachment) -> str:
        if request.GET.get("referer") == "settings":
            url = reverse("misago:account-attachments")
            if request.GET.get("cursor"):
                url += "?cursor=" + request.GET["cursor"]
            return url

        if request.GET.get("referer") == "post" and attachment.post:
            return attachment.post.get_absolute_url()

        return reverse("misago:index")


def _get_referer_querystring(request: HttpRequest, attachment: Attachment) -> str:
    if request.GET.get("referer") == "settings":
        querystring = "?referer=settings"
        if request.GET.get("cursor"):
            querystring += "?cursor=" + request.GET["cursor"]
        return querystring

    if request.GET.get("referer") == "post" and attachment.post:
        return "?referer=post"

    return ""


class AttachmentsUploadView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            self.check_permissions(request)
        except PermissionDenied as error:
            return JsonResponse({"error": str(error)}, status=403)

        attachments, error = self.process_uploads(request)

        data = {}
        return JsonResponse(data)

    def check_permissions(self, request: HttpRequest):
        if request.settings.allowed_attachment_types == AllowedAttachments.NONE:
            raise PermissionDenied(
                pgettext("attachments upload", "Attachment uploads are disabled")
            )

        if not request.user.is_authenticated:
            raise PermissionDenied(
                pgettext("attachments upload", "Sign in to upload attachments")
            )

        if (
            request.user_permissions.can_upload_attachments
            == CanUploadAttachments.NEVER
        ):
            raise PermissionDenied(
                pgettext("attachments upload", "You can't upload attachments")
            )

    def process_uploads(
        self, request: HttpRequest
    ) -> tuple[list[Attachment], ValidationError | None]:
        return handle_attachments_upload(request, request.FILES.getlist("upload"))


attachment_delete = AttachmentDeleteView.as_view()
attachment_details = AttachmentDetailsView.as_view()
attachment_download = AttachmentDownloadView.as_view()
attachment_thumbnail = AttachmentThumbnailView.as_view()
attachments_upload = AttachmentsUploadView.as_view()
