import pytest
from django.urls import reverse

from ...test import assert_contains, assert_not_contains

attachments_url = reverse("misago:admin:attachments:index")


def test_attachments_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, attachments_url)


def test_attachments_list_renders_empty(admin_client):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, "No attachments exist.")


def test_attachments_list_renders_temp_txt_attachment(
    admin_client, text_file, attachment_factory
):
    attachment = attachment_factory(text_file)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.filename)


def test_attachments_list_renders_txt_attachment(
    admin_client, text_file, user, post, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, post=post)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.filename)
    assert_contains(response, post.thread.title)


def test_attachments_list_renders_temp_image_attachment(
    admin_client, image_small, attachment_factory
):
    attachment = attachment_factory(image_small)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.filename)


def test_attachments_list_renders_image_attachment(
    admin_client, image_small, user, post, attachment_factory
):
    attachment = attachment_factory(image_small, uploader=user, post=post)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.filename)
    assert_contains(response, post.thread.title)


def test_attachments_list_renders_temp_image_with_thumbnail_attachment(
    admin_client, image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.filename)
    assert_contains(response, attachment.thumbnail.url)


def test_attachments_list_renders_image_with_thumbnail_attachment(
    admin_client, image_large, image_small, user, post, attachment_factory
):
    attachment = attachment_factory(
        image_large, thumbnail_path=image_small, uploader=user, post=post
    )

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.filename)
    assert_contains(response, attachment.thumbnail.url)
    assert_contains(response, post.thread.title)


def test_attachments_list_searches_attachment_by_uploader(
    admin_client, text_file, image_small, user, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(attachments_url + f"?redirected=1&uploader={user.slug}")
    assert_contains(response, attachment.filename)
    assert_not_contains(response, attachment_other.filename)


def test_attachments_list_searches_attachment_by_filename(
    admin_client, text_file, image_small, user, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(
        attachments_url + f"?redirected=1&filename={attachment.filename}"
    )
    assert_contains(response, attachment.filename)
    assert_not_contains(response, attachment_other.filename)


def test_attachments_list_searches_attachment_by_filetype(
    admin_client, text_file, image_small, user, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(
        attachments_url + f"?redirected=1&filetype={attachment.filetype_name}"
    )
    assert_contains(response, attachment.filename)
    assert_not_contains(response, attachment_other.filename)


def test_attachments_list_searches_not_orphaned_attachments(
    admin_client, text_file, image_small, user, post, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(attachments_url + f"?redirected=1&is_orphan=no")
    assert_contains(response, attachment.filename)
    assert_not_contains(response, attachment_other.filename)


def test_attachments_list_searches_orphaned_attachments(
    admin_client, text_file, image_small, user, post, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(attachments_url + f"?redirected=1&is_orphan=yes")
    assert_not_contains(response, attachment.filename)
    assert_contains(response, attachment_other.filename)
