from typing import Protocol, cast

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.module_loading import import_string
from django.views import View

from ..permissions.attachments import check_download_attachment_permission
from .hooks import get_attachment_details_page_context_data_hook
from .models import Attachment


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
        return {"attachment": attachment}


attachment_details = AttachmentDetailsView.as_view()
attachment_download = AttachmentDownloadView.as_view()
attachment_thumbnail = AttachmentThumbnailView.as_view()
