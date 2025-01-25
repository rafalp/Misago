import json

from ..serialize import serialize_attachment


def test_serialize_attachment_serializes_attachment(user, user_attachment):
    user_attachment.dimensions = "400x150"
    user_attachment.upload = "attachments/img.png"
    user_attachment.thumbnail = "attachments/thumbnail.png"
    user_attachment.thumbnail_size = 256 * 1024

    data = serialize_attachment(user_attachment)

    assert json.dumps(data)
    assert data["id"] == user_attachment.id
    assert data["secret"] == user_attachment.secret
    assert data["name"] == user_attachment.name
    assert data["url"] == user_attachment.get_details_url()
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


def test_serialize_attachment_serializes_anonymous_user_attachment(attachment):
    attachment.dimensions = "400x150"
    attachment.upload = "attachments/img.png"
    attachment.thumbnail = "attachments/thumbnail.png"
    attachment.thumbnail_size = 256 * 1024

    data = serialize_attachment(attachment)

    assert json.dumps(data)
    assert data["id"] == attachment.id
    assert data["secret"] == attachment.secret
    assert data["name"] == attachment.name
    assert data["url"] == attachment.get_details_url()
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


def test_serialize_attachment_serializes_attachment_without_dimensions(attachment):
    data = serialize_attachment(attachment)

    assert json.dumps(data)
    assert data["dimensions"] is None


def test_serialize_attachment_serializes_attachment_without_upload(attachment):
    data = serialize_attachment(attachment)

    assert json.dumps(data)
    assert data["upload"] is None


def test_serialize_attachment_serializes_attachment_without_thumbnail(attachment):
    data = serialize_attachment(attachment)

    assert json.dumps(data)
    assert data["thumbnail"] is None
