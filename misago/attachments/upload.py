from io import BytesIO

from PIL import Image, UnidentifiedImageError
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import pgettext

from ..core.utils import slugify
from .filename import clean_filename, trim_filename
from .filetypes import AttachmentFileType
from .hooks import get_attachment_plugin_data_hook
from .models import Attachment
from .thumbnails import generate_attachment_thumbnail
from .validators import (
    get_attachments_storage_constraints,
    validate_uploaded_file,
    validate_uploaded_file_extension,
)


def handle_attachments_upload(
    request: HttpRequest,
    uploads: list[UploadedFile],
    keys: list[str] | None = None,
) -> tuple[list[Attachment], ValidationError | None]:
    if keys is not None:
        if len(keys) != len(uploads):
            raise ValidationError(
                message=pgettext(
                    "attachments upload", "'keys' and 'uploads' must have same length"
                ),
                code="upload_handler",
            )
        if len(keys) != len(set(keys)):
            raise ValidationError(
                message=pgettext("attachments upload", "'keys' must be unique"),
                code="upload_handler",
            )

    storage_constraints = get_attachments_storage_constraints(
        request.settings.unused_attachments_storage_limit,
        request.user_permissions,
    )

    extensions = request.settings.restrict_attachments_extensions.split()
    extensions_restriction = request.settings.restrict_attachments_extensions_type

    errors_list: list[ValidationError] = []
    errors_dict: dict[str, ValidationError] = {}
    attachments: list[Attachment] = []

    for i, upload in enumerate(uploads):
        upload_key = None
        if keys:
            upload_key = keys[i]

        try:
            filetype = validate_uploaded_file(
                upload,
                allowed_attachments=request.settings.allowed_attachment_types,
                max_size=request.user_permissions.attachment_size_limit,
                **storage_constraints,
            )

            if extensions:
                validate_uploaded_file_extension(
                    upload, extensions_restriction, extensions
                )

            attachment = store_uploaded_file(request, upload, filetype)
            attachment.upload_key = upload_key
            attachments.append(attachment)

            attachment_size = attachment.size + attachment.thumbnail_size
            storage_constraints["storage_left"] = max(
                storage_constraints["storage_left"] - attachment_size, 0
            )
        except ValidationError as error:
            if upload_key:
                errors_dict[upload_key] = error
            else:
                errors_list.append(error)

    if errors_list or errors_dict:
        return attachments, ValidationError(errors_list or errors_dict)

    return attachments, None


def store_uploaded_file(
    request: HttpRequest, upload: UploadedFile, filetype: AttachmentFileType
) -> Attachment:
    clean_name = clean_filename(upload.name, filetype, max_length=200)

    attachment = Attachment.objects.create(
        uploader=request.user,
        uploader_name=request.user.username,
        uploader_slug=request.user.slug,
        uploaded_at=timezone.now(),
        name=clean_name,
        slug=slugify(clean_name),
        filetype_id=filetype.id,
        size=upload.size,
    )

    upload.name = trim_filename(upload.name, filetype)

    if filetype.is_image:
        _store_attachment_image(request, attachment, upload, filetype)
    else:
        attachment.upload = upload
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

    image_format = image.format
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
        image.save(image_stream, image_format)
        upload = SimpleUploadedFile(
            upload.name, image_stream.getvalue(), upload.content_type
        )
        del image_stream

    attachment.upload = upload
    attachment.dimensions = "x".join(map(str, image.size))

    thumbnail_width = request.settings.attachment_thumbnail_width
    thumbnail_height = request.settings.attachment_thumbnail_height

    if image.width > thumbnail_width or image.height > thumbnail_height:
        generate_attachment_thumbnail(
            attachment, image, thumbnail_width, thumbnail_height
        )


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
