from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...readtracker.models import ReadCategory, ReadThread


def test_thread_post_unread_view_returns_redirect_to_first_post_for_unread_thread(
    thread_reply_factory, user_client, thread
):
    thread_reply_factory(thread)
    thread_reply_factory(thread)
    thread_reply_factory(thread)

    response = user_client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{thread.first_post_id}"
    )


def test_thread_post_unread_view_returns_redirect_to_first_visible_unread_post_using_read_category(
    thread_reply_factory, user_client, user, thread
):
    last_read = thread_reply_factory(thread)
    thread_reply_factory(thread, is_unapproved=True)
    reply = thread_reply_factory(thread)
    thread_reply_factory(thread)

    ReadCategory.objects.create(
        user=user, category=thread.category, read_time=last_read.posted_at
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_post_unread_view_returns_redirect_to_first_visible_unread_post_using_read_thread(
    thread_reply_factory, user_client, user, thread
):
    last_read = thread_reply_factory(thread)
    thread_reply_factory(thread, is_unapproved=True)
    reply = thread_reply_factory(thread)
    thread_reply_factory(thread)

    ReadThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=last_read.posted_at,
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_post_unread_view_returns_redirect_to_last_post_for_read_thread(
    thread_reply_factory, user_client, user, thread
):
    thread_reply_factory(thread)
    thread_reply_factory(thread)
    last_post = thread_reply_factory(thread)

    ReadThread.objects.create(
        user=user,
        category=thread.category,
        thread=thread,
        read_time=last_post.posted_at,
    )

    response = user_client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{last_post.id}"
    )


def test_thread_post_unread_view_returns_redirect_to_last_post_for_anonymous_user(
    thread_reply_factory, client, thread
):
    thread_reply_factory(thread)
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_post_unread_view_returns_error_404_if_thread_doesnt_exist(db, client):
    response = client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": 1, "slug": "invalid"},
        )
    )

    assert response.status_code == 404


def test_thread_post_unread_view_returns_error_404_if_user_cant_see_thread(
    client, thread
):
    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 404


def test_thread_post_unread_view_returns_error_403_if_user_cant_see_thread_contents(
    client, thread
):
    thread.category.delay_browse_check = True
    thread.category.save()

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = client.get(
        reverse(
            "misago:thread-post-unread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 403


def test_thread_post_unread_view_returns_error_404_if_thread_is_private(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-post-unapproved",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert response.status_code == 404
