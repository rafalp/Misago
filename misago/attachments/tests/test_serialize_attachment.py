import json

from ..serialize import serialize_attachment


def test_serialize_attachment_serializes_user_attachment(user, user_image_attachment):
    user_image_attachment.dimensions = "400x150"
    user_image_attachment.upload = "attachments/img.png"
    user_image_attachment.thumbnail = "attachments/thumbnail.png"
    user_image_attachment.thumbnail_size = 256 * 1024
    user_image_attachment.thumbnail_dimensions = "100x75"

    data = serialize_attachment(user_image_attachment)

    assert json.dumps(data)
    assert data["id"] == user_image_attachment.id
    assert data["key"] is None
    assert data["name"] == user_image_attachment.name
    assert data["url"] == user_image_attachment.get_details_url()
    assert data["uploader"] == {"id": user.id, "username": user.username}
    assert data["filetype"] == {
        "id": "png",
        "is_media": True,
        "is_video": False,
        "name": "PNG image",
    }
    assert data["dimensions"] == [400, 150]
    assert data["upload"] == {
        "size": {"bytes": 1048576, "formatted": "1.0\xa0MB"},
        "url": "/media/attachments/img.png",
    }
    assert data["thumbnail"] == {
        "size": {"bytes": 262144, "formatted": "256.0\xa0KB"},
        "url": "/media/attachments/thumbnail.png",
    }


def test_serialize_attachment_serializes_anonymous_user_attachment(image_attachment):
    image_attachment.dimensions = "400x150"
    image_attachment.upload = "attachments/img.png"
    image_attachment.thumbnail = "attachments/thumbnail.png"
    image_attachment.thumbnail_size = 256 * 1024
    image_attachment.thumbnail_dimensions = "100x75"

    data = serialize_attachment(image_attachment)

    assert json.dumps(data)
    assert data["id"] == image_attachment.id
    assert data["key"] is None
    assert data["name"] == image_attachment.name
    assert data["url"] == image_attachment.get_details_url()
    assert data["uploader"] == {"id": None, "username": "Anonymous"}
    assert data["filetype"] == {
        "id": "png",
        "is_media": True,
        "is_video": False,
        "name": "PNG image",
    }
    assert data["dimensions"] == [400, 150]
    assert data["upload"] == {
        "size": {"bytes": 1048576, "formatted": "1.0\xa0MB"},
        "url": "/media/attachments/img.png",
    }
    assert data["thumbnail"] == {
        "size": {"bytes": 262144, "formatted": "256.0\xa0KB"},
        "url": "/media/attachments/thumbnail.png",
    }


def test_serialize_attachment_serializes_attachment_without_dimensions(text_attachment):
    data = serialize_attachment(text_attachment)

    assert json.dumps(data)
    assert data["dimensions"] is None


def test_serialize_attachment_serializes_attachment_without_upload(
    broken_text_attachment,
):
    data = serialize_attachment(broken_text_attachment)

    assert json.dumps(data)
    assert data["upload"] is None


def test_serialize_attachment_serializes_attachment_without_thumbnail(image_attachment):
    data = serialize_attachment(image_attachment)

    assert json.dumps(data)
    assert data["thumbnail"] is None


def test_serialize_attachment_serializes_attachment_with_upload_key(text_attachment):
    text_attachment.upload_key = "test"
    data = serialize_attachment(text_attachment)

    assert json.dumps(data)
    assert data["key"] == "test"
