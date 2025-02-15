import pytest

from ..servers import (
    django_file_response,
    django_redirect_response,
    nginx_x_accel_redirect,
)


def test_django_file_response_serves_file(text_file, attachment_factory):
    attachment = attachment_factory(text_file)
    response = django_file_response(None, attachment)

    assert response.status_code == 200
    assert response["Content-Type"] == "text/plain"
    assert response["Content-Disposition"] == 'inline; filename="textfile.txt"'
    assert response["Content-Length"] == str(attachment.size)

    with open(attachment.upload.path, "rb") as fp:
        assert b"".join(response.streaming_content) == fp.read()


def test_django_file_response_raises_value_error_for_missing_upload(
    broken_text_attachment,
):
    with pytest.raises(ValueError) as exc_info:
        django_file_response(None, broken_text_attachment)

    assert str(exc_info.value) == "Required 'Attachment.upload' attribute is 'None'."


def test_django_file_response_serves_thumbnail(
    image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)
    response = django_file_response(None, attachment, thumbnail=True)

    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert response["Content-Disposition"] == 'inline; filename="image_large.png"'
    assert response["Content-Length"] == str(attachment.thumbnail_size)

    with open(attachment.thumbnail.path, "rb") as fp:
        assert b"".join(response.streaming_content) == fp.read()


def test_django_file_response_raises_value_error_for_missing_thumbnail(
    image_attachment,
):
    with pytest.raises(ValueError) as exc_info:
        django_file_response(None, image_attachment, thumbnail=True)

    assert str(exc_info.value) == "Required 'Attachment.thumbnail' attribute is 'None'."


def test_django_redirect_response_serves_file(text_file, attachment_factory):
    attachment = attachment_factory(text_file)
    response = django_redirect_response(None, attachment)

    assert response.status_code == 301
    assert response["Location"] == attachment.upload.url


def test_django_redirect_response_raises_value_error_for_missing_upload(
    broken_text_attachment,
):
    with pytest.raises(ValueError) as exc_info:
        django_redirect_response(None, broken_text_attachment)

    assert str(exc_info.value) == "Required 'Attachment.upload' attribute is 'None'."


def test_django_redirect_response_serves_thumbnail(
    image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)
    response = django_redirect_response(None, attachment, thumbnail=True)

    assert response.status_code == 301
    assert response["Location"] == attachment.thumbnail.url


def test_django_redirect_response_raises_value_error_for_missing_thumbnail(
    image_attachment,
):
    with pytest.raises(ValueError) as exc_info:
        django_redirect_response(None, image_attachment, thumbnail=True)

    assert str(exc_info.value) == "Required 'Attachment.thumbnail' attribute is 'None'."


def test_nginx_x_accel_redirect_serves_file(text_file, attachment_factory):
    attachment = attachment_factory(text_file)
    response = nginx_x_accel_redirect(None, attachment)

    assert response.status_code == 200
    assert response["Content-Type"] == "text/plain"
    assert response["Content-Disposition"] == 'inline; filename="textfile.txt"'
    assert response["Content-Length"] == str(attachment.size)
    assert response["X-Accel-Redirect"] == attachment.upload.url


def test_nginx_x_accel_redirect_skips_content_length_if_upload_size_is_zero(
    text_file, attachment_factory
):
    attachment = attachment_factory(text_file)
    attachment.size = 0

    response = nginx_x_accel_redirect(None, attachment)

    assert response.status_code == 200
    assert response["Content-Type"] == "text/plain"
    assert response["Content-Disposition"] == 'inline; filename="textfile.txt"'
    assert response["X-Accel-Redirect"] == attachment.upload.url

    assert "Content-Length" not in response.headers


def test_nginx_x_accel_redirect_raises_value_error_for_missing_upload(
    broken_text_attachment,
):
    with pytest.raises(ValueError) as exc_info:
        nginx_x_accel_redirect(None, broken_text_attachment)

    assert str(exc_info.value) == "Required 'Attachment.upload' attribute is 'None'."


def test_nginx_x_accel_redirect_serves_thumbnail(
    image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)
    response = nginx_x_accel_redirect(None, attachment, thumbnail=True)

    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert response["Content-Disposition"] == 'inline; filename="image_large.png"'
    assert response["Content-Length"] == str(attachment.thumbnail_size)
    assert response["X-Accel-Redirect"] == attachment.thumbnail.url


def test_nginx_x_accel_redirect_skips_content_length_if_thumbnail_size_is_zero(
    image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)
    attachment.thumbnail_size = 0

    response = nginx_x_accel_redirect(None, attachment, thumbnail=True)

    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    assert response["Content-Disposition"] == 'inline; filename="image_large.png"'
    assert response["X-Accel-Redirect"] == attachment.thumbnail.url

    assert "Content-Length" not in response.headers


def test_nginx_x_accel_redirect_raises_value_error_for_missing_thumbnail(
    image_attachment,
):
    with pytest.raises(ValueError) as exc_info:
        nginx_x_accel_redirect(None, image_attachment, thumbnail=True)

    assert str(exc_info.value) == "Required 'Attachment.thumbnail' attribute is 'None'."
