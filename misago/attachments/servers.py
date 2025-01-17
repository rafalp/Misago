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
    file = attachment.thumbnail if thumbnail else attachment.upload
    return HttpResponsePermanentRedirect(file.url)


def django_file_response(
    request: HttpRequest, attachment: Attachment, thumbnail: bool = False
) -> HttpResponse:
    file = attachment.thumbnail if thumbnail else attachment.upload

    response = FileResponse(
        open(file.path, "rb"),
        filename=attachment.name,
        as_attachment=attachment.filetype.as_attachment,
        content_type=attachment.content_type,
    )

    if thumbnail and attachment.thumbnail_size:
        response["Content-Length"] = attachment.thumbnail_size
    elif attachment.size:
        response["Content-Length"] = attachment.size

    return response


def nginx_x_accel_redirect(
    request: HttpRequest, attachment: Attachment, thumbnail: bool = False
) -> HttpResponse:
    response = HttpResponse()

    if attachment.filetype.as_attachment:
        response["Content-Disposition"] = "attachment; filename=" + attachment.name
    else:
        response["Content-Disposition"] = "inline; filename=" + attachment.name

    response["Content-Type"] = attachment.content_type

    file = attachment.thumbnail if thumbnail else attachment.upload
    response["X-Accel-Redirect"] = file.url

    if thumbnail and attachment.thumbnail_size:
        response["Content-Length"] = attachment.thumbnail_size
    elif attachment.size:
        response["Content-Length"] = attachment.size

    return response
