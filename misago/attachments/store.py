from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest
from django.utils import timezone

from .filetypes import AttachmentFileType
from .models import Attachment


def store_attachment_file(
    request: HttpRequest, file: UploadedFile, filetype: AttachmentFileType
) -> Attachment:
    attachment = Attachment.objects.create(
        uploader=request.user,
        uploader_name=request.user.username,
        uploader_slug=request.user.slug,
        uploaded_at=timezone.now(),
        secret=Attachment.generate_new_secret(),
        filename=file.name,
        size=file.size,
        filetype_name=filetype.name,
    )

    if filetype.is_image:
        attachment.set_image(file)
    elif filetype.is_video:
        attachment.set_video(file)
    else:
        attachment.set_file(file)

    attachment.save()

    return attachment
