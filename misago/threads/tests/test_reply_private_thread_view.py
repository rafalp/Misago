from django.urls import reverse

from ...readtracker.models import ReadCategory
from ...readtracker.tracker import mark_thread_read
from ...test import assert_contains, assert_not_contains


def test_reply_private_thread_view_displays_login_page_to_guests(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, "Sign in to reply to threads")


def test_reply_private_thread_view_displays_error_page_to_users_without_private_threads_permission(
    user, user_client, user_private_thread
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t use private threads.",
        status_code=403,
    )


def test_reply_private_thread_view_displays_error_page_to_user_who_cant_see_private_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": private_thread.id, "slug": private_thread.slug},
        )
    )
    assert response.status_code == 404


def test_reply_private_thread_view_displays_reply_thread_form(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, "Reply to thread")


def test_reply_private_thread_view_posts_new_thread_reply(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
        )
        + f"#post-{user_private_thread.last_post_id}"
    )


def test_reply_private_thread_view_posts_new_thread_reply_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    user_private_thread.refresh_from_db()
    assert (
        response["hx-redirect"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
        )
        + f"#post-{user_private_thread.last_post_id}"
    )


def test_reply_private_thread_view_posts_new_thread_reply_in_quick_reply(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
        },
    )
    assert response.status_code == 302

    user_private_thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.pk, "slug": user_private_thread.slug},
        )
        + f"#post-{user_private_thread.last_post_id}"
    )


def test_reply_private_thread_view_posts_new_thread_reply_in_quick_reply_with_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    user_private_thread.refresh_from_db()
    assert_contains(response, f"post-{user_private_thread.last_post_id}")
    assert_contains(response, f"<p>How&#x27;s going?</p>")


def test_reply_private_thread_view_posted_reply_in_quick_reply_with_htmx_is_read(
    user, user_client, user_private_thread
):
    mark_thread_read(user, user_private_thread, user_private_thread.last_post.posted_on)

    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    user_private_thread.refresh_from_db()
    assert_contains(response, f"post-{user_private_thread.last_post_id}")
    assert_contains(response, f"<p>How&#x27;s going?</p>")

    ReadCategory.objects.get(
        user=user,
        category=user_private_thread.category,
        read_time=user_private_thread.last_post_on,
    )


def test_reply_private_thread_view_previews_message(user_client, user_private_thread):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_reply_private_thread_view_previews_message_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "preview": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_reply_private_thread_view_previews_message_in_quick_reply(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
            "preview": "true",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Message preview")


def test_reply_private_thread_view_previews_message_in_quick_reply_with_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
            "preview": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Message preview")


def test_reply_private_thread_view_validates_post(user_client, user_private_thread):
    response = user_client.post(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_reply_private_thread_view_shows_error_if_thread_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:reply-private-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
    )

    assert_not_contains(response, "Reply to thread", status_code=404)
    assert_not_contains(response, thread.title, status_code=404)
