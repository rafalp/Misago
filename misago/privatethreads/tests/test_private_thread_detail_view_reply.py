from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains, assert_not_contains
from ..models import PrivateThreadMember


def test_private_thread_detail_view_shows_reply_button_to_user(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response,
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )


def test_private_thread_detail_view_shows_quick_reply_to_user(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "quick_reply")


def test_private_thread_detail_view_doesnt_show_reply_ui_to_user_in_closed_thread(
    user_client, other_user_private_thread
):
    other_user_private_thread.is_closed = True
    other_user_private_thread.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "This thread is locked.")


def test_private_thread_detail_view_doesnt_show_quick_reply_to_user_in_thread_without_other_members(
    user_client, user, other_user_private_thread
):
    PrivateThreadMember.objects.exclude(user=user).delete()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response, "You can&#x27;t reply to a private thread without other members"
    )


def test_private_thread_detail_view_shows_reply_ui_to_private_threads_moderator_in_closed_thread(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    other_user_private_thread.is_closed = True
    other_user_private_thread.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response,
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )


def test_private_thread_detail_view_shows_reply_ui_to_private_threads_moderator_in_thread_without_other_members(
    user_client, user, other_user_private_thread
):
    PrivateThreadMember.objects.exclude(user=user).delete()

    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response,
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )
    assert_not_contains(
        response, "You can&#x27;t reply to a private thread without other members"
    )


def test_private_thread_detail_view_shows_reply_ui_to_global_moderator_in_closed_thread(
    moderator_client, other_user_private_thread
):
    other_user_private_thread.is_closed = True
    other_user_private_thread.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response,
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )


def test_private_thread_detail_view_shows_reply_ui_to_private_threads_moderator_in_thread_without_other_members(
    moderator_client, moderator, other_user_private_thread
):
    PrivateThreadMember.objects.exclude(user=moderator).delete()

    Moderator.objects.create(
        user=moderator,
        is_global=False,
        private_threads=True,
    )

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response,
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )
    assert_not_contains(
        response, "You can&#x27;t reply to a private thread without other members"
    )
