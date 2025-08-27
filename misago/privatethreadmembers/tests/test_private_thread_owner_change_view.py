from django.urls import reverse

from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
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
        kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == other_user
    assert members == [user, other_user, moderator]

    ThreadUpdate.objects.get(
        actor=user,
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
