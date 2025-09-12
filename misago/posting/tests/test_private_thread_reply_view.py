from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...readtracker.models import ReadCategory
from ...readtracker.tracker import mark_thread_read
from ...test import assert_contains
from ..formsets import Formset


def test_thread_reply_view_displays_login_page_to_guests(
    client, other_user_private_thread
):
    response = client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to reply to threads")


def test_private_thread_reply_view_displays_error_403_to_users_without_private_threads_permission(
    user_client, members_group, other_user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_reply_view_displays_error_404_to_users_without_thread_access(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_reply_view_displays_posting_form(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_reply_view_posts_new_reply(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_reply_view_posts_new_reply_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    reply = other_user_private_thread.post_set.last()

    assert (
        response["hx-redirect"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_reply_view_posts_new_reply_in_quick_reply(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )


def test_private_thread_reply_view_posts_new_reply_in_quick_reply_with_htmx(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    reply = other_user_private_thread.post_set.last()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, f"<p>This is a reply!</p>")


def test_private_thread_reply_view_posted_reply_in_quick_reply_with_htmx_is_read(
    user_client, user, other_user_private_thread
):
    mark_thread_read(
        user, other_user_private_thread, other_user_private_thread.last_post.posted_at
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    reply = other_user_private_thread.post_set.last()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, f"<p>This is a reply!</p>")

    ReadCategory.objects.get(
        user=user,
        category=other_user_private_thread.category,
        read_time=reply.posted_at,
    )


def test_private_thread_reply_view_previews_message(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_previews_message_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_previews_message_in_quick_reply(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_previews_message_in_quick_reply_with_htmx(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_validates_post(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_private_thread_reply_view_validates_posted_contents(
    user_client, other_user_private_thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Your message contains spam!")


@override_dynamic_settings(merge_concurrent_posts=0)
def test_private_thread_reply_view_runs_flood_control(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    thread_reply_factory(other_user_private_thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a flood message",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(
        response, "You can&#x27;t post a new message so soon after the previous one."
    )


def test_private_thread_reply_view_merges_reply_with_users_recent_post(
    thread_reply_factory, user, user_client, other_user_private_thread
):
    reply = thread_reply_factory(
        other_user_private_thread, poster=user, original="Previous message"
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    assert reply.original == "Previous message\n\nReply contents"
