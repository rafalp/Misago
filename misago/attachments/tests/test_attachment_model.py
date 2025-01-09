from pathlib import Path

from ..models import Attachment


def test_attachment_delete_deletes_file(user, text_file, attachment_factory):
    attachment = attachment_factory(text_file, uploader=user)

    file_path = Path(attachment.file.path)
    assert file_path.exists()

    attachment.delete()

    assert not file_path.exists()


def test_attachment_delete_deletes_image(user, image_small, attachment_factory):
    attachment = attachment_factory(image_small, uploader=user)

    image_path = Path(attachment.image.path)
    assert image_path.exists()

    attachment.delete()

    assert not image_path.exists()


def test_attachment_delete_deletes_image_thumbnail(
    user, image_large, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_large, uploader=user, thumbnail_path=image_small
    )

    image_path = Path(attachment.image.path)
    assert image_path.exists()

    thumbnail_path = Path(attachment.thumbnail.path)
    assert thumbnail_path.exists()

    attachment.delete()

    assert not image_path.exists()
    assert not thumbnail_path.exists()
