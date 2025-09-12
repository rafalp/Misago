from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments, CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...readtracker.models import ReadCategory
from ...readtracker.tracker import mark_thread_read
from ...test import assert_contains
from ..formsets import Formset


def test_thread_reply_view_displays_login_page_to_guests(client, thread):
    response = client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to reply to threads")


def test_thread_reply_view_displays_error_404_to_users_without_see_category_permission(
    user_client, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404


def test_thread_reply_view_displays_error_404_to_users_without_browse_category_permission(
    user_client, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert response.status_code == 404


def test_thread_reply_view_displays_error_404_to_users_who_cant_see_thread(
    user_client, user, hidden_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": hidden_thread.id, "slug": hidden_thread.slug},
        )
    )
    assert response.status_code == 404


def test_thread_reply_view_displays_error_403_to_users_without_reply_category_permission(
    user_client, user, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "You can&#x27;t reply to threads in this category.", 403)


def test_thread_reply_view_displays_error_403_to_users_without_reply_in_closed_category_permission(
    user_client, default_category, thread
):
    default_category.is_closed = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "This category is closed.", 403)


def test_thread_reply_view_displays_error_403_to_users_without_reply_in_closed_thread_permission(
    user_client, thread
):
    thread.is_closed = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )
    assert_contains(response, "This thread is closed.", 403)


def test_thread_reply_view_displays_posting_form(user_client, thread):
    response = user_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, thread.title)


def test_thread_reply_view_displays_posting_form_to_users_with_unapproved_thread_access(
    moderator_client, unapproved_thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": unapproved_thread.id,
                "slug": unapproved_thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, unapproved_thread.title)


def test_thread_reply_view_displays_posting_form_to_users_with_hidden_thread_access(
    moderator_client, hidden_thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": hidden_thread.id,
                "slug": hidden_thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, hidden_thread.title)


def test_thread_reply_view_displays_posting_form_to_users_with_reply_in_closed_category_permission(
    moderator_client, default_category, thread
):
    default_category.is_closed = True
    default_category.save()

    response = moderator_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, thread.title)


def test_thread_reply_view_displays_posting_form_to_users_with_reply_in_closed_thread_permission(
    moderator_client, thread
):
    thread.is_closed = True
    thread.save()

    response = moderator_client.get(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, thread.title)


def test_thread_reply_view_posts_new_reply(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
        },
    )
    assert response.status_code == 302

    reply = thread.post_set.last()

    assert (
        response["location"]
        == reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + f"#post-{reply.id}"
    )


def test_thread_reply_view_posts_new_reply_in_htmx(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    reply = thread.post_set.last()

    assert (
        response["hx-redirect"]
        == reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + f"#post-{reply.id}"
    )


def test_thread_reply_view_posts_new_reply_in_quick_reply(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
    )
    assert response.status_code == 302

    reply = thread.post_set.last()

    assert (
        response["location"]
        == reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + f"#post-{reply.id}"
    )


def test_thread_reply_view_posts_new_reply_in_quick_reply_with_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    reply = thread.post_set.last()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, f"<p>This is a reply!</p>")


def test_thread_reply_view_posted_reply_in_quick_reply_with_htmx_is_read(
    user_client, user, thread
):
    mark_thread_read(user, thread, thread.last_post.posted_at)

    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    reply = thread.post_set.last()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, f"<p>This is a reply!</p>")

    ReadCategory.objects.get(
        user=user,
        category=thread.category,
        read_time=reply.posted_at,
    )


def test_thread_reply_view_previews_message(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_thread_reply_view_previews_message_in_htmx(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_thread_reply_view_previews_message_in_quick_reply(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_thread_reply_view_previews_message_in_quick_reply_with_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
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


def test_thread_reply_view_validates_post(user_client, thread):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_thread_reply_view_validates_posted_contents(
    user_client, thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Your message contains spam!")


@override_dynamic_settings(merge_concurrent_posts=0)
def test_thread_reply_view_runs_flood_control(
    thread_reply_factory, user_client, user, thread
):
    thread_reply_factory(thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "This is a flood message",
        },
    )
    assert_contains(response, "Post reply")
    assert_contains(
        response, "You can&#x27;t post a new message so soon after the previous one."
    )


def test_thread_reply_view_merges_reply_with_users_recent_post(
    thread_reply_factory, user, user_client, thread
):
    reply = thread_reply_factory(thread, poster=user, original="Previous message")

    response = user_client.post(
        reverse(
            "misago:thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    reply.refresh_from_db()

    assert (
        response["location"]
        == reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
        + f"#post-{reply.id}"
    )

    assert reply.original == "Previous message\n\nReply contents"


def test_thread_reply_view_merges_reply_with_users_recent_post_in_htmx(
    thread_reply_factory, user, user_client, thread
):
    reply = thread_reply_factory(thread, poster=user, original="Previous message")

    response = user_client.post(
        reverse(
            "misago:thread-reply",
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

    reply.refresh_from_db()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, reply.parsed)

    assert reply.original == "Previous message\n\nReply contents"
