from django.http import Http404, HttpRequest, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views import View

from ..permissions.attachments import check_download_attachment_permission
from .models import Attachment


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
        response = FileResponse(
            open(attachment.upload.path, "rb"),
            filename=attachment.name,
        )
        response.headers["Content-Type"] = attachment.content_type
        return response


class AttachmentThumbnailView(AttachmentView):
    def create_response(
        self, request: HttpRequest, attachment: Attachment
    ) -> HttpResponse:
        if not attachment.thumbnail:
            raise Http404()

        response = FileResponse(
            open(attachment.thumbnail.path, "rb"),
            filename=attachment.name,
        )
        response.headers["Content-Type"] = attachment.content_type
        return response


attachment_download = AttachmentDownloadView.as_view()
attachment_thumbnail = AttachmentThumbnailView.as_view()
