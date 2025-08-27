import json

from django.urls import reverse

from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ...users.bans import ban_user
from ..members import get_private_thread_members


def test_private_thread_owner_change_view_displays_confirm_page_on_get(
    user_client, other_user, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert_contains(
        response,
        "Are you sure you want to make <strong>Other_User</strong> the new thread owner?",
    )


def test_private_thread_owner_change_view_displays_confirm_page_on_get_for_moderator(
    moderator_client, other_user, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert_contains(
        response,
        "Are you sure you want to make <strong>Other_User</strong> the new thread owner?",
    )


def test_private_thread_owner_change_view_changes_thread_owner(
    user_client, user, other_user, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == other_user
    assert members == [user, other_user, moderator]

    ThreadUpdate.objects.get(
        actor=user,
        thread=user_private_thread,
        action=ThreadUpdateActionName.CHANGED_OWNER,
    )


def test_private_thread_owner_change_view_changes_thread_owner_for_moderator(
    moderator_client, user, other_user, moderator, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == other_user
    assert members == [user, other_user, moderator]

    ThreadUpdate.objects.get(
        actor=moderator,
        thread=user_private_thread,
        action=ThreadUpdateActionName.CHANGED_OWNER,
    )


def test_private_thread_owner_change_view_changes_thread_owner_in_htmx(
    user_client, user, other_user, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "3 members")

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == other_user
    assert members == [user, other_user, moderator]

    ThreadUpdate.objects.get(
        actor=user,
        thread=user_private_thread,
        action=ThreadUpdateActionName.CHANGED_OWNER,
    )


def test_private_thread_owner_change_view_does_nothing_if_member_is_already_owner(
    moderator_client, user, other_user, moderator, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": user.id,
            },
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, other_user, moderator]

    assert not ThreadUpdate.objects.exists()


def test_private_thread_owner_change_view_returns_403_if_user_cant_use_private_threads(
    user_client, members_group, other_user
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": 1,
                "slug": "thread",
                "user_id": other_user.id,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_owner_change_view_returns_404_if_thread_doesnt_exist(
    user_client, other_user
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": 1,
                "slug": "thread",
                "user_id": other_user.id,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_owner_change_view_returns_404_if_user_is_not_thread_member(
    user_client, other_user, private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": private_thread.id,
                "slug": private_thread.slug,
                "user_id": other_user.id,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_owner_change_view_returns_redirect_if_member_doesnt_exist(
    user_client, other_user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id * 10,
            },
        ),
    )
    assert response.status_code == 302


def test_private_thread_owner_change_view_returns_404_if_member_doesnt_exist_in_htmx(
    user_client, other_user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id * 10,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert json.loads(response.content) == {"error": "Member doesn't exist"}


def test_private_thread_owner_change_view_returns_403_if_user_is_not_thread_owner(
    other_user_client, other_user, user_private_thread
):
    response = other_user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t change this thread&#x27;s owner.", 403)


def test_private_thread_owner_change_view_returns_403_if_member_cant_be_made_owner(
    user_client, other_user, user_private_thread
):
    ban_user(other_user)

    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        ),
    )
    assert_contains(response, "his user is banned", 403)


def test_private_thread_owner_change_view_returns_404_if_thread_is_not_private(
    user_client, other_user, thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-owner-change",
            kwargs={
                "id": thread.id,
                "slug": thread.slug,
                "user_id": other_user.id,
            },
        ),
    )
    assert response.status_code == 404
