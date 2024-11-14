from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


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
