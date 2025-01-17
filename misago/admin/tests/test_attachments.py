import pytest
from django.urls import reverse

from ...attachments.models import Attachment
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
    assert_contains(response, attachment.name)


def test_attachments_list_renders_txt_attachment(
    admin_client, text_file, user, post, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, post=post)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.name)
    assert_contains(response, post.thread.title)


def test_attachments_list_renders_temp_image_attachment(
    admin_client, image_small, attachment_factory
):
    attachment = attachment_factory(image_small)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.name)


def test_attachments_list_renders_image_attachment(
    admin_client, image_small, user, post, attachment_factory
):
    attachment = attachment_factory(image_small, uploader=user, post=post)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.name)
    assert_contains(response, post.thread.title)


def test_attachments_list_renders_temp_image_with_thumbnail_attachment(
    admin_client, image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_thumbnail_url())


def test_attachments_list_renders_image_with_thumbnail_attachment(
    admin_client, image_large, image_small, user, post, attachment_factory
):
    attachment = attachment_factory(
        image_large, thumbnail_path=image_small, uploader=user, post=post
    )

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, attachment.name)
    assert_contains(response, attachment.get_thumbnail_url())
    assert_contains(response, post.thread.title)


def test_attachments_list_searches_attachment_by_uploader(
    admin_client, text_file, image_small, user, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(attachments_url + f"?redirected=1&uploader={user.slug}")
    assert_contains(response, attachment.name)
    assert_not_contains(response, attachment_other.name)


def test_attachments_list_searches_attachment_by_name(
    admin_client, text_file, image_small, user, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(
        attachments_url + f"?redirected=1&name={attachment.name}"
    )
    assert_contains(response, attachment.name)
    assert_not_contains(response, attachment_other.name)


def test_attachments_list_searches_attachment_by_filetype(
    admin_client, text_file, image_small, user, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment_other = attachment_factory(image_small)

    response = admin_client.get(
        attachments_url + f"?redirected=1&filetype={attachment.filetype_id}"
    )
    assert_contains(response, attachment.name)
    assert_not_contains(response, attachment_other.name)


def test_attachments_list_searches_posted_attachments(
    admin_client, text_file, user, post, attachment_factory
):
    attachment_posted = attachment_factory(
        text_file, name="posted.txt", uploader=user, post=post
    )
    attachment_deleted = attachment_factory(
        text_file, name="deleted.txt", uploader=user, is_deleted=True
    )
    attachment_unused = attachment_factory(text_file, name="unused.txt")

    response = admin_client.get(attachments_url + f"?redirected=1&status=posted")
    assert_contains(response, attachment_posted.name)
    assert_not_contains(response, attachment_deleted.name)
    assert_not_contains(response, attachment_unused.name)


def test_attachments_list_searches_unused_attachments(
    admin_client, text_file, user, post, attachment_factory
):
    attachment_posted = attachment_factory(
        text_file, name="posted.txt", uploader=user, post=post
    )
    attachment_deleted = attachment_factory(
        text_file, name="deleted.txt", uploader=user, is_deleted=True
    )
    attachment_unused = attachment_factory(text_file, name="unused.txt")

    response = admin_client.get(attachments_url + f"?redirected=1&status=unused")
    assert_not_contains(response, attachment_posted.name)
    assert_not_contains(response, attachment_deleted.name)
    assert_contains(response, attachment_unused.name)


def test_attachments_list_searches_deleted_attachments(
    admin_client, text_file, user, post, attachment_factory
):
    attachment_posted = attachment_factory(
        text_file, name="posted.txt", uploader=user, post=post
    )
    attachment_deleted = attachment_factory(
        text_file, name="deleted.txt", uploader=user, is_deleted=True
    )
    attachment_unused = attachment_factory(text_file, name="unused.txt")

    response = admin_client.get(attachments_url + f"?redirected=1&status=deleted")
    assert_not_contains(response, attachment_posted.name)
    assert_contains(response, attachment_deleted.name)
    assert_not_contains(response, attachment_unused.name)


def test_attachments_list_deletes_attachments(
    admin_client, text_file, image_small, user, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment_other = attachment_factory(image_small)

    response = admin_client.post(
        attachments_url,
        data={
            "action": "delete",
            "selected_items": [str(attachment.id), str(attachment_other.id)],
        },
    )
    assert response.status_code == 302

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()

    with pytest.raises(Attachment.DoesNotExist):
        attachment_other.refresh_from_db()
