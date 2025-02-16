from django.urls import reverse

from ...test import assert_contains, assert_not_contains
from ..models import ThreadParticipant


def test_private_thread_replies_view_shows_error_on_missing_permission(
    user, user_client, user_private_thread
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_not_contains(response, user_private_thread.title, status_code=403)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=403,
    )


def test_private_thread_replies_view_shows_error_to_anonymous_user(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_not_contains(response, user_private_thread.title, status_code=403)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=403,
    )


def test_private_thread_replies_view_shows_error_to_user_who_is_not_thread_participant(
    user, user_client, user_private_thread
):
    ThreadParticipant.objects.filter(user=user).delete()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, user_private_thread.title, status_code=404)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=404,
    )


def test_private_thread_replies_view_shows_thread_to_user(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_other_users_thread_to_user(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_thread_to_user_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_other_users_thread_to_user_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_user_private_thread.first_post.parsed)


def test_private_thread_replies_view_redirects_if_slug_is_invalid(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": "invalid"},
        ),
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )


def test_private_thread_replies_view_ignores_invalid_slug_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": "invalid"},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_redirects_to_last_page_if_page_number_is_too_large(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 1000,
            },
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
    )


def test_private_thread_replies_view_shows_last_page_if_page_number_is_too_large_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 1000,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_post_with_attachments(
    user_client,
    user_private_thread,
    image_attachment,
    image_thumbnail_attachment,
    video_attachment,
    text_attachment,
):
    post = user_private_thread.first_post

    image_attachment.associate_with_post(post)
    image_attachment.save()

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    video_attachment.associate_with_post(post)
    video_attachment.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_replies_view_shows_post_with_embed_attachments(
    user_client,
    user_private_thread,
    image_attachment,
    image_thumbnail_attachment,
    video_attachment,
    text_attachment,
):
    post = user_private_thread.first_post

    invalid_id = (
        max(
            image_attachment.id,
            image_thumbnail_attachment.id,
            video_attachment.id,
            text_attachment.id,
        )
        * 100
    )

    post.parsed = (
        "<p>Hello world!</>"
        f"<attachment={image_attachment.name}:{image_attachment.slug}:{image_attachment.id}>"
        f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.slug}:{image_thumbnail_attachment.id}>"
        f"<attachment={video_attachment.name}:{video_attachment.slug}:{video_attachment.id}>"
        f"<attachment={text_attachment.name}:{text_attachment.slug}:{text_attachment.id}>"
        f"<attachment=invalid-attachment.txt:invalid-attachment-txt:{invalid_id}>"
    )
    post.metadata = {
        "attachments": [
            image_attachment.id,
            image_thumbnail_attachment.id,
            video_attachment.id,
            text_attachment.id,
        ],
    }
    post.save()

    image_attachment.associate_with_post(post)
    image_attachment.save()

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    video_attachment.associate_with_post(post)
    video_attachment.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, user_private_thread.title)
    assert_not_contains(response, post.parsed)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_replies_view_shows_error_if_regular_thread_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
    )
    assert_not_contains(response, thread.title, status_code=404)
    assert_not_contains(response, thread.first_post.parsed, status_code=404)
