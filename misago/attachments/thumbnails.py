from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Attachment


def generate_attachment_thumbnail(
    attachment: Attachment, image, image_format: str, width: int, height: int
):
    thumbnail_stream = BytesIO()

    image.thumbnail((width, height))
    image.save(thumbnail_stream, image_format)

    attachment.thumbnail = SimpleUploadedFile(
        attachment.name,
        thumbnail_stream.getvalue(),
        attachment.content_type,
    )

    attachment.thumbnail_dimensions = "x".join(map(str, image.size))
    attachment.thumbnail_size = attachment.thumbnail.size

    del thumbnail_stream
