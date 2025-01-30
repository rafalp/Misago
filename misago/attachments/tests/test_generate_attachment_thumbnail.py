from PIL import Image

from ..thumbnails import generate_attachment_thumbnail


def test_generate_attachment_thumbnail_generates_thumbnail_image_and_updates_attachment(
    attachment, image_large, teardown_attachments
):
    image = Image.open(image_large)
    generate_attachment_thumbnail(attachment, image, 400, 300)

    assert attachment.thumbnail
    assert attachment.thumbnail.url
    assert attachment.thumbnail_dimensions == "300x300"
    assert attachment.thumbnail_size
