def test_attachment_download_returns_server_response(
    user, user_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    response = user_client.get(attachment.get_absolute_url())

    assert response.status_code == 301
    assert response["location"] == attachment.upload.url


def test_attachment_download_returns_404_response_if_upload_is_missing(
    user, user_client, user_attachment
):
    response = user_client.get(user_attachment.get_absolute_url())
    assert response.status_code == 404


def test_attachment_thumbnail_returns_server_response(
    user, user_client, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_small, uploader=user, thumbnail_path=image_small
    )
    response = user_client.get(attachment.get_thumbnail_url())

    assert response.status_code == 301
    assert response["location"] == attachment.thumbnail.url


def test_attachment_thumbnail_returns_404_response_if_thumbnail_is_missing(
    user, user_client, image_small, attachment_factory
):
    attachment = attachment_factory(image_small, uploader=user)
    response = user_client.get(attachment.get_thumbnail_url())

    assert response.status_code == 404
