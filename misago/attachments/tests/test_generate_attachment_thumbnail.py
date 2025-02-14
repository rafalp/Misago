from PIL import Image

from ..thumbnails import generate_attachment_thumbnail


def test_generate_attachment_thumbnail_generates_thumbnail_image_and_updates_attachment(
    image_attachment, image_large, teardown_attachments
):
    image = Image.open(image_large)
    generate_attachment_thumbnail(image_attachment, image, 400, 300)

    assert image_attachment.thumbnail
    assert image_attachment.thumbnail.url
    assert image_attachment.thumbnail_dimensions == "300x300"
    assert image_attachment.thumbnail_size
