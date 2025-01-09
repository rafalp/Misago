from io import BytesIO
from math import ceil

from PIL import Image, UnidentifiedImageError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import pgettext

from .filetypes import AttachmentFileType
from .hooks import get_attachment_plugin_data_hook
from .models import Attachment


def store_uploaded_file(
    request: HttpRequest, upload: UploadedFile, filetype: AttachmentFileType
) -> Attachment:
    attachment = Attachment.objects.create(
        uploader=request.user,
        uploader_name=request.user.username,
        uploader_slug=request.user.slug,
        uploaded_at=timezone.now(),
        secret=Attachment.get_new_secret(),
        filename=upload.name,
        size=upload.size,
        filetype_name=filetype.name,
    )

    if filetype.is_image:
        _store_attachment_image(request, attachment, upload, filetype)
    else:
        if filetype.is_video:
            attachment.video = upload
        else:
            attachment.file = upload
        attachment.plugin_data = get_attachment_plugin_data(request, upload)

    attachment.save()

    return attachment


def _store_attachment_image(
    request: HttpRequest,
    attachment: Attachment,
    upload: UploadedFile,
    filetype: AttachmentFileType,
):
    try:
        image = Image.open(upload)
    except UnidentifiedImageError:
        raise ValidationError(
            message=pgettext("image opening error", "Image file is not valid."),
            code="unidentified_image",
        )

    attachment.plugin_data = get_attachment_plugin_data(request, upload, image)

    max_width = request.settings.attachment_image_max_width
    max_height = request.settings.attachment_image_max_height

    if image.width > max_width or image.height > max_height:
        if image.width > max_width:
            aspect = float(max_width) / float(image.width)
            new_size = (max_width, max(int(image.height * aspect), 1))
            image = image.resize(new_size)
        if image.height > max_height:
            aspect = float(max_height) / float(image.height)
            new_size = (max(int(image.width * aspect), 1), max_height)
            image = image.resize(new_size)

        image_stream = BytesIO()
        image.save(image_stream, filetype.extensions[0])
        upload = SimpleUploadedFile(
            upload.name, image_stream.read(), upload.content_type
        )
        del image_stream

    attachment.image = upload
    attachment.dimensions = "x".join(map(str, image.size))

    thumbnail_width = request.settings.attachment_thumbnail_width
    thumbnail_height = request.settings.attachment_thumbnail_height

    if image.width > thumbnail_width or image.height > thumbnail_height:
        image.thumbnail((thumbnail_width, thumbnail_height))
        thumbnail_stream = BytesIO()
        image.save(thumbnail_stream, filetype.extensions[0])
        attachment.thumbnail = SimpleUploadedFile(
            upload.name, thumbnail_stream.read(), upload.content_type
        )
        del thumbnail_stream


def get_attachment_plugin_data(
    request: HttpRequest,
    upload: UploadedFile,
    image: Image.Image | None = None,
) -> dict:
    return get_attachment_plugin_data_hook(
        _get_attachment_plugin_data_action, request, upload, image
    )


def _get_attachment_plugin_data_action(
    request: HttpRequest,
    upload: UploadedFile,
    image: Image.Image | None = None,
) -> dict:
    return {}
