import pytest
from django.urls import reverse

from ...test import assert_contains
from ...threads.models import Thread
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..members import get_private_thread_members
from ..models import PrivateThreadMember


def test_private_thread_leave_view_displays_confirm_page_on_get_for_thread_owner(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Are you sure you want to leave this thread?")


def test_private_thread_leave_view_displays_confirm_page_on_get_for_member(
    other_user_client, user_private_thread
):
    response = other_user_client.get(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Are you sure you want to leave this thread?")


def test_private_thread_leave_view_displays_confirm_page_on_get_for_moderator(
    moderator_client, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Are you sure you want to leave this thread?")


def test_private_thread_leave_view_removes_thread_owner(
    user_client, user, other_user, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    owner, members = get_private_thread_members(user_private_thread)
    assert owner is None
    assert members == [other_user, moderator]

    ThreadUpdate.objects.get(
        actor=user,
        thread=user_private_thread,
        action=ThreadUpdateActionName.LEFT,
    )

    user_private_thread.refresh_from_db()


def test_private_thread_leave_view_removes_thread_member(
    other_user_client, user, other_user, moderator, user_private_thread
):
    response = other_user_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, moderator]

    ThreadUpdate.objects.get(
        actor=other_user,
        thread=user_private_thread,
        action=ThreadUpdateActionName.LEFT,
    )

    user_private_thread.refresh_from_db()


def test_private_thread_leave_view_removes_thread_moderator(
    moderator_client, user, other_user, moderator, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, other_user]

    ThreadUpdate.objects.get(
        actor=moderator,
        thread=user_private_thread,
        action=ThreadUpdateActionName.LEFT,
    )

    user_private_thread.refresh_from_db()


def test_private_thread_member_deletes_thread_when_last_member_leaves(
    user_client, user, user_private_thread
):
    PrivateThreadMember.objects.exclude(user=user).delete()
    assert PrivateThreadMember.objects.count() == 1

    response = user_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    owner, members = get_private_thread_members(user_private_thread)
    assert owner is None
    assert members == []

    with pytest.raises(Thread.DoesNotExist):
        user_private_thread.refresh_from_db()


def test_private_thread_leave_view_returns_403_if_user_cant_use_private_threads(
    user_client, members_group
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": 1,
                "slug": "thread",
            },
        ),
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_leave_view_returns_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": 1,
                "slug": "thread",
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_leave_view_returns_404_if_user_cant_access_thread(
    user_client, private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_leave_view_returns_404_if_thread_is_not_private(
    user_client, thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-leave",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
    )
    assert response.status_code == 404
