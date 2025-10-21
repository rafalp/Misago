import json

from django.urls import reverse

from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..members import get_private_thread_members


def test_private_thread_member_remove_view_displays_confirm_page_on_get_for_thread_owner(
    user_client, other_user, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert_contains(
        response,
        "Are you sure you want to remove <strong>Other_User</strong> from this thread?",
    )


def test_private_thread_member_remove_view_displays_confirm_page_on_get_for_moderator(
    moderator_client, other_user, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert_contains(
        response,
        "Are you sure you want to remove <strong>Other_User</strong> from this thread?",
    )


def test_private_thread_member_remove_view_removes_thread_member(
    user_client, user, other_user, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, moderator]

    ThreadUpdate.objects.get(
        actor=user,
        thread=user_private_thread,
        action=ThreadUpdateActionName.REMOVED_MEMBER,
    )


def test_private_thread_member_remove_view_removes_thread_member_for_moderator(
    moderator_client, user, other_user, moderator, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, moderator]

    ThreadUpdate.objects.get(
        actor=moderator,
        thread=user_private_thread,
        action=ThreadUpdateActionName.REMOVED_MEMBER,
    )


def test_private_thread_member_remove_view_returns_redirect_to_next_url(
    user_client, other_user, user_private_thread
):
    next_url = reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "page": 42,
        },
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        ),
        {"next": next_url},
    )
    assert response.status_code == 302
    assert response["location"] == next_url


def test_private_thread_member_remove_view_returns_redirect_to_thread_if_next_url_is_invalid(
    user_client, other_user, user_private_thread
):
    next_url = reverse(
        "misago:thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "page": 42,
        },
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        ),
        {"next": next_url},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )


def test_private_thread_member_remove_view_removes_thread_member_in_htmx(
    user_client, user, other_user, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id,
            },
        ),
        headers={"hx-request": "true"},
    )

    assert_contains(response, "2 members")

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, moderator]

    ThreadUpdate.objects.get(
        actor=user,
        thread=user_private_thread,
        action=ThreadUpdateActionName.REMOVED_MEMBER,
    )


def test_private_thread_member_remove_view_does_nothing_if_user_tries_to_delete_themselves(
    user_client, user, other_user, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": user.id,
            },
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    owner, members = get_private_thread_members(user_private_thread)
    assert owner == user
    assert members == [user, other_user, moderator]

    assert not ThreadUpdate.objects.exists()


def test_private_thread_member_remove_view_returns_403_if_user_cant_use_private_threads(
    user_client, members_group, other_user
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": 1,
                "slug": "thread",
                "user_id": other_user.id,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_member_remove_view_returns_404_if_thread_doesnt_exist(
    user_client, other_user
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": 1,
                "slug": "thread",
                "user_id": other_user.id,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_member_remove_view_returns_404_if_user_cant_access_thread(
    user_client, other_user, private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
                "user_id": other_user.id,
            },
        ),
    )
    assert response.status_code == 404


def test_private_thread_member_remove_view_returns_redirect_if_member_doesnt_exist(
    user_client, other_user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id * 10,
            },
        ),
    )
    assert response.status_code == 302


def test_private_thread_member_remove_view_returns_404_if_member_doesnt_exist_in_htmx(
    user_client, other_user, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": other_user.id * 10,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert json.loads(response.content) == {"error": "Member doesn't exist"}


def test_private_thread_member_remove_view_returns_403_if_user_is_not_thread_owner(
    other_user_client, other_user, moderator, user_private_thread
):
    response = other_user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": moderator.id,
            },
        ),
    )
    assert_contains(response, "You can&#x27;t remove this member.", 403)


def test_private_thread_member_remove_view_returns_403_if_member_cant_be_removed(
    user_client, moderator, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "user_id": moderator.id,
            },
        ),
    )
    assert_contains(
        response, "This member is a moderator. You can&#x27;t remove them", 403
    )


def test_private_thread_member_remove_view_returns_404_if_thread_is_not_private(
    user_client, other_user, thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-member-remove",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "user_id": other_user.id,
            },
        ),
    )
    assert response.status_code == 404
