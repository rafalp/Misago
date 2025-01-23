from django.http import (
    FileResponse,
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
)

from .models import Attachment


def django_redirect_response(
    request: HttpRequest, attachment: Attachment, thumbnail: bool = False
) -> HttpResponse:
    file = _get_django_file(attachment, thumbnail)
    response = HttpResponsePermanentRedirect(file.url)
    response["Cache-Control"] = "max-age=31536000, immutable"
    return response


def django_file_response(
    request: HttpRequest, attachment: Attachment, thumbnail: bool = False
) -> HttpResponse:
    file = _get_django_file(attachment, thumbnail)

    return FileResponse(
        open(file.path, "rb"),
        filename=attachment.name,
        as_attachment=attachment.filetype.as_attachment,
        content_type=attachment.content_type,
    )


def nginx_x_accel_redirect(
    request: HttpRequest, attachment: Attachment, thumbnail: bool = False
) -> HttpResponse:
    response = HttpResponse(content_type=attachment.content_type)

    if attachment.filetype.as_attachment:
        response["Content-Disposition"] = f'attachment; filename="{attachment.name}"'
    else:
        response["Content-Disposition"] = f'inline; filename="{attachment.name}"'

    file = _get_django_file(attachment, thumbnail)
    response["X-Accel-Redirect"] = file.url

    if thumbnail and attachment.thumbnail_size:
        response["Content-Length"] = attachment.thumbnail_size
    elif not thumbnail and attachment.size:
        response["Content-Length"] = attachment.size

    return response


def _get_django_file(attachment: Attachment, thumbnail: bool = False):
    if thumbnail:
        if not attachment.thumbnail:
            raise ValueError(f"Required 'Attachment.thumbnail' attribute is 'None'.")

        return attachment.thumbnail

    if not attachment.upload:
        raise ValueError(f"Required 'Attachment.upload' attribute is 'None'.")

    return attachment.upload
