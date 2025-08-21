import pytest

from PIL import Image

from ..thumbnails import generate_attachment_thumbnail


def test_generate_attachment_thumbnail_generates_thumbnail_image_and_updates_attachment(
    image_attachment, image_large, teardown_attachments
):
    image = Image.open(image_large)
    generate_attachment_thumbnail(image_attachment, image, image.format, 400, 300)

    assert image_attachment.thumbnail
    assert image_attachment.thumbnail.url
    assert image_attachment.thumbnail_dimensions == "300x300"
    assert image_attachment.thumbnail_size
    assert image_attachment.thumbnail_format == image.format


@pytest.mark.parametrize(
    [
        "img_height",
        "img_width",
    ],
    [
        pytest.param(1000, 400, id="max_height_greater"),
        pytest.param(400, 1000, id="max_width_greater"),
    ],
)
def test_generate_attachment_thumbnail_generates_thumbnail_image_and_updates_attachment_gt_max_dimensions(
    img_height, img_width, image_attachment, image_large, teardown_attachments
):
    image = Image.open(image_large)
    generate_attachment_thumbnail(
        image_attachment, image, image.format, img_width, img_height
    )

    assert image_attachment.thumbnail
    assert image_attachment.thumbnail.url
    assert image_attachment.thumbnail_dimensions == "400x400"
    assert image_attachment.thumbnail_size
    assert image_attachment.thumbnail_format == image.format
