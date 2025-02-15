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


def test_attachments_list_renders_broken_text_attachment(
    admin_client, broken_text_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, broken_text_attachment.name)


def test_attachments_list_renders_broken_image_attachment(
    admin_client, broken_image_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, broken_image_attachment.name)


def test_attachments_list_renders_broken_video_attachment(
    admin_client, broken_video_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, broken_video_attachment.name)


def test_attachments_list_renders_text_attachment(admin_client, text_attachment):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_details_url())


def test_attachments_list_renders_image_attachment(admin_client, image_attachment):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_attachment.get_details_url())


def test_attachments_list_renders_image_attachment_with_thumbnail(
    admin_client, image_thumbnail_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, image_thumbnail_attachment.name)
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_details_url())


def test_attachments_list_renders_video_attachment(admin_client, video_attachment):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, video_attachment.name)
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_details_url())


def test_attachments_list_renders_user_text_attachment(
    admin_client, user_text_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, user_text_attachment.name)
    assert_contains(response, user_text_attachment.get_absolute_url())
    assert_contains(response, user_text_attachment.get_details_url())


def test_attachments_list_renders_user_image_attachment(
    admin_client, user_image_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, user_image_attachment.name)
    assert_contains(response, user_image_attachment.get_absolute_url())
    assert_contains(response, user_image_attachment.get_details_url())


def test_attachments_list_renders_user_image_attachment_with_thumbnail(
    admin_client, user_image_thumbnail_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, user_image_thumbnail_attachment.name)
    assert_contains(response, user_image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, user_image_thumbnail_attachment.get_details_url())


def test_attachments_list_renders_user_video_attachment(
    admin_client, user_video_attachment
):
    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, user_video_attachment.name)
    assert_contains(response, user_video_attachment.get_absolute_url())
    assert_contains(response, user_video_attachment.get_details_url())


def test_attachments_list_renders_posted_text_attachment(
    admin_client, text_attachment, thread, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_details_url())
    assert_contains(response, thread.title)
    assert_contains(response, post.get_absolute_url())


def test_attachments_list_renders_posted_image_attachment(
    admin_client, image_attachment, thread, post
):
    image_attachment.associate_with_post(post)
    image_attachment.save()

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_attachment.get_details_url())
    assert_contains(response, thread.title)
    assert_contains(response, post.get_absolute_url())


def test_attachments_list_renders_posted_image_attachment_with_thumbnail(
    admin_client, image_thumbnail_attachment, thread, post
):
    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, image_thumbnail_attachment.name)
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_details_url())
    assert_contains(response, thread.title)
    assert_contains(response, post.get_absolute_url())


def test_attachments_list_renders_posted_video_attachment(
    admin_client, video_attachment, thread, post
):
    video_attachment.associate_with_post(post)
    video_attachment.save()

    response = admin_client.get(attachments_url + "?redirected=1")
    assert_contains(response, video_attachment.name)
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_details_url())
    assert_contains(response, thread.title)
    assert_contains(response, post.get_absolute_url())


def test_attachments_list_searches_attachment_by_uploader(
    admin_client,
    other_user,
    text_attachment,
    user_text_attachment,
    other_user_text_attachment,
):
    response = admin_client.get(
        attachments_url + f"?redirected=1&uploader={other_user.slug}"
    )
    assert_contains(response, other_user_text_attachment.get_absolute_url())
    assert_not_contains(response, user_text_attachment.get_absolute_url())
    assert_not_contains(response, text_attachment.get_absolute_url())


def test_attachments_list_searches_attachment_by_name(
    admin_client, text_attachment, image_attachment
):
    response = admin_client.get(
        attachments_url + f"?redirected=1&name={text_attachment.name}"
    )
    assert_contains(response, text_attachment.get_absolute_url())
    assert_not_contains(response, image_attachment.get_absolute_url())


def test_attachments_list_searches_attachment_by_filetype(
    admin_client, text_attachment, image_attachment
):
    response = admin_client.get(
        attachments_url + f"?redirected=1&filetype={text_attachment.filetype_id}"
    )
    assert_contains(response, text_attachment.get_absolute_url())
    assert_not_contains(response, image_attachment.get_absolute_url())


def test_attachments_list_searches_posted_attachments(
    admin_client, text_attachment, image_attachment, post
):
    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = admin_client.get(attachments_url + f"?redirected=1&status=posted")
    assert_contains(response, text_attachment.get_absolute_url())
    assert_not_contains(response, image_attachment.get_absolute_url())


def test_attachments_list_searches_unused_attachments(
    admin_client, text_attachment, image_attachment, post
):
    image_attachment.associate_with_post(post)
    image_attachment.save()

    response = admin_client.get(attachments_url + f"?redirected=1&status=unused")
    assert_contains(response, text_attachment.get_absolute_url())
    assert_not_contains(response, image_attachment.get_absolute_url())


def test_attachments_list_searches_deleted_attachments(
    admin_client, text_attachment, image_attachment
):
    text_attachment.is_deleted = True
    text_attachment.save()

    response = admin_client.get(attachments_url + f"?redirected=1&status=deleted")
    assert_contains(response, text_attachment.get_absolute_url())
    assert_not_contains(response, image_attachment.get_absolute_url())


def test_attachments_list_searches_broken_attachments(
    admin_client, broken_text_attachment, image_attachment
):
    response = admin_client.get(attachments_url + f"?redirected=1&status=broken")
    assert_contains(response, broken_text_attachment.name)
    assert_not_contains(response, image_attachment.get_absolute_url())


def test_attachments_list_deletes_broken_attachments(
    admin_client, broken_text_attachment
):
    response = admin_client.post(
        attachments_url,
        data={
            "action": "delete",
            "selected_items": [str(broken_text_attachment.id)],
        },
    )
    assert response.status_code == 302

    with pytest.raises(Attachment.DoesNotExist):
        broken_text_attachment.refresh_from_db()


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
