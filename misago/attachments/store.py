from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest
from django.utils import timezone

from .filetypes import AttachmentFileType
from .models import Attachment


def store_uploaded_file(
    request: HttpRequest, upload: UploadedFile, filetype: AttachmentFileType
) -> Attachment:
    attachment = Attachment.objects.create(
        uploader=request.user,
        uploader_name=request.user.username,
        uploader_slug=request.user.slug,
        uploaded_at=timezone.now(),
        secret=Attachment.generate_new_secret(),
        filename=upload.name,
        size=upload.size,
        filetype_name=filetype.name,
    )

    if filetype.is_image:
        _set_attachment_image(request, attachment, upload, filetype)
    elif filetype.is_video:
        attachment.video = upload
    else:
        attachment.file = upload

    attachment.save()

    return attachment


def _set_attachment_image(
    request: HttpRequest,
    attachment: Attachment,
    upload: UploadedFile,
    filetype: AttachmentFileType,
):
    attachment.set_image(upload)
