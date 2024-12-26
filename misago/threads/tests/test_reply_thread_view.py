from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...readtracker.models import ReadCategory
from ...readtracker.tracker import mark_thread_read
from ...test import assert_contains, assert_not_contains
from ..test import reply_thread


def test_reply_thread_view_displays_login_page_to_guests(client, thread):
    response = client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "Sign in to reply to threads")


def test_reply_thread_view_displays_error_page_to_users_without_see_category_permission(
    user_client, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404


def test_reply_thread_view_displays_error_page_to_users_without_browse_category_permission(
    user_client, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404


def test_reply_thread_view_displays_error_page_to_users_without_reply_threads_permission(
    user_client, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(
        response, "You can&#x27;t reply to threads in this category.", status_code=403
    )


def test_reply_thread_view_displays_error_page_to_users_without_post_in_closed_category_permission(
    user_client, thread
):
    thread.category.is_closed = True
    thread.category.save()

    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(
        response,
        "This category is closed.",
        status_code=403,
    )


def test_reply_thread_view_displays_error_page_to_users_without_post_in_closed_thread_permission(
    user_client, thread
):
    thread.is_closed = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(
        response,
        "This thread is closed.",
        status_code=403,
    )


def test_reply_thread_view_displays_reply_thread_form(user_client, thread):
    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "Reply to thread")


def test_reply_thread_view_displays_reply_thread_form_to_users_with_permission_to_post_in_closed_category(
    user, user_client, thread, members_group, moderators_group
):
    thread.category.is_closed = True
    thread.category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "Reply to thread")


def test_reply_thread_view_displays_reply_thread_form_to_users_with_permission_to_post_in_closed_thread(
    user, user_client, thread, members_group, moderators_group
):
    thread.is_closed = True
    thread.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "Reply to thread")


def test_reply_thread_view_posts_new_thread_reply(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )


def test_reply_thread_view_posts_new_thread_reply_in_htmx(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    thread.refresh_from_db()
    assert (
        response["hx-redirect"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )


def test_reply_thread_view_posts_new_thread_reply_in_quick_reply(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )


def test_reply_thread_view_posts_new_thread_reply_in_quick_reply_with_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    thread.refresh_from_db()
    assert_contains(response, f"post-{thread.last_post_id}")
    assert_contains(response, f"<p>How&#x27;s going?</p>")


def test_reply_thread_view_posted_reply_in_quick_reply_with_htmx_is_read(
    user, user_client, thread
):
    mark_thread_read(user, thread, thread.last_post.posted_on)

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    thread.refresh_from_db()
    assert_contains(response, f"post-{thread.last_post_id}")
    assert_contains(response, f"<p>How&#x27;s going?</p>")

    ReadCategory.objects.get(
        user=user,
        category=thread.category,
        read_time=thread.last_post_on,
    )


def test_reply_thread_view_previews_message(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_reply_thread_view_previews_message_in_htmx(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {"posting-post-post": "How's going?", "preview": "true"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_reply_thread_view_previews_message_in_quick_reply(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "How's going?",
            "quick_reply": "true",
            "preview": "true",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Message preview")


def test_reply_thread_view_previews_message_in_quick_reply_with_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
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


def test_reply_thread_view_validates_post(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_reply_thread_view_validates_posted_contents(
    user_client, thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Your message contains spam!")


def test_reply_thread_view_appends_reply_to_user_recent_post(user, user_client, thread):
    reply = reply_thread(thread, user, message="Previous message")

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.original == "Previous message\n\nReply contents"


def test_reply_thread_view_appends_reply_to_user_recent_post_in_quick_reply_with_htmx(
    user, user_client, thread
):
    reply = reply_thread(thread, user, message="Previous message")

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, reply.parsed)

    reply.refresh_from_db()
    assert reply.original == "Previous message\n\nReply contents"


@override_dynamic_settings(merge_concurrent_posts=0, flood_control=0)
def test_reply_thread_view_doesnt_append_reply_to_user_recent_post_if_feature_is_disabled(
    user, user_client, thread
):
    reply = reply_thread(thread, user, message="Previous message")

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )

    reply.refresh_from_db()
    assert reply.original == "Previous message"
    assert thread.last_post_id > reply.id


@override_dynamic_settings(flood_control=0)
def test_reply_thread_view_doesnt_append_reply_to_user_recent_post_in_preview(
    user, user_client, thread
):
    reply_thread(thread, user, message="Previous message")

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
            "preview": "true",
        },
    )
    assert response.status_code == 200
    assert_contains(response, "<p>Reply contents</p>")
    assert_not_contains(response, "<p>Previous message</p>")


@override_dynamic_settings(merge_concurrent_posts=1)
def test_reply_thread_view_doesnt_append_reply_to_user_recent_post_if_recent_post_is_too_old(
    user, user_client, thread
):
    reply = reply_thread(
        thread,
        user,
        message="Previous message",
        posted_on=timezone.now() - timedelta(minutes=2),
    )

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )

    reply.refresh_from_db()
    assert reply.original == "Previous message"
    assert thread.last_post_id > reply.id


@override_dynamic_settings(flood_control=0)
def test_reply_thread_view_doesnt_append_reply_to_user_recent_post_if_recent_post_is_by_other_user(
    other_user, user_client, thread
):
    reply = reply_thread(thread, other_user, message="Previous message")

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )

    reply.refresh_from_db()
    assert reply.original == "Previous message"
    assert thread.last_post_id > reply.id


@override_dynamic_settings(flood_control=0)
def test_reply_thread_view_doesnt_append_reply_to_user_recent_post_if_recent_post_is_hidden(
    user, user_client, thread
):
    reply = reply_thread(
        thread,
        user,
        message="Previous message",
        is_hidden=True,
    )

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )

    reply.refresh_from_db()
    assert reply.original == "Previous message"
    assert thread.last_post_id > reply.id


@override_dynamic_settings(flood_control=0)
def test_reply_thread_view_doesnt_append_reply_to_user_recent_post_if_recent_post_is_not_editable(
    user, user_client, thread
):
    reply = reply_thread(
        thread,
        user,
        message="Previous message",
        is_protected=True,
    )

    response = user_client.post(
        reverse(
            "misago:reply-thread",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"id": thread.pk, "slug": thread.slug},
        )
        + f"#post-{thread.last_post_id}"
    )

    reply.refresh_from_db()
    assert reply.original == "Previous message"
    assert thread.last_post_id > reply.id


def test_reply_thread_view_shows_error_if_private_thread_is_accessed(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:reply-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )

    assert_not_contains(response, "Reply to thread", status_code=404)
    assert_not_contains(response, user_private_thread.title, status_code=404)
