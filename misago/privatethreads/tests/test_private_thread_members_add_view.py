import pytest
from django.urls import reverse

from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..models import PrivateThreadMember


@pytest.fixture
def mock_notify_on_new_private_thread(mocker):
    return mocker.patch(
        "misago.privatethreads.views.members.notify_on_new_private_thread"
    )


def test_private_thread_members_add_view_renders_form(user_client, user_private_thread):
    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Add members")


def test_private_thread_members_add_view_renders_form_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Add members")


def test_private_thread_members_add_view_does_nothing_if_new_users_are_members_already(
    mock_notify_on_new_private_thread,
    user,
    user_client,
    user_private_thread,
    other_user,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"users": [user.username, other_user.username]},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    PrivateThreadMember.objects.get(thread=user_private_thread, user=other_user)

    assert not ThreadUpdate.objects.exists()

    mock_notify_on_new_private_thread.delay.assert_not_called()


def test_private_thread_members_add_view_adds_new_thread_members(
    mock_notify_on_new_private_thread, user, user_client, user_private_thread, admin
):
    response = user_client.post(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"users": [admin.username]},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    PrivateThreadMember.objects.get(thread=user_private_thread, user=admin)

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.ADDED_MEMBER,
        context=admin.username,
    )

    mock_notify_on_new_private_thread.delay.assert_called_once_with(
        user.id, user_private_thread.id, [admin.id]
    )


def test_private_thread_members_add_view_adds_new_thread_members_using_noscript_fallback(
    mock_notify_on_new_private_thread, user, user_client, user_private_thread, admin
):
    response = user_client.post(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"users_noscript": admin.username},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    PrivateThreadMember.objects.get(thread=user_private_thread, user=admin)

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.ADDED_MEMBER,
        context=admin.username,
    )

    mock_notify_on_new_private_thread.delay.assert_called_once_with(
        user.id, user_private_thread.id, [admin.id]
    )


def test_private_thread_members_add_view_adds_new_thread_members_in_htmx(
    mock_notify_on_new_private_thread, user, user_client, user_private_thread, admin
):
    response = user_client.post(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"users": [admin.username]},
        headers={"hx-request": "true"},
    )

    assert_contains(response, "4 members")
    assert_contains(response, admin.username)

    PrivateThreadMember.objects.get(thread=user_private_thread, user=admin)

    ThreadUpdate.objects.get(
        thread=user_private_thread,
        action=ThreadUpdateActionName.ADDED_MEMBER,
        context=admin.username,
    )

    mock_notify_on_new_private_thread.delay.assert_called_once_with(
        user.id, user_private_thread.id, [admin.id]
    )


def test_private_thread_members_add_view_returns_redirect_to_next_thread_url(
    mock_notify_on_new_private_thread, user, user_client, user_private_thread, admin
):
    next_url = (
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
        + "?next=true"
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "users": [admin.username],
            "next": next_url,
        },
    )

    assert response.status_code == 302
    assert response["location"] == next_url


def test_private_thread_members_add_view_returns_redirect_to_default_thread_url_if_next_url_is_invalid(
    mock_notify_on_new_private_thread, user, user_client, user_private_thread, admin
):
    response = user_client.post(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "users": [admin.username],
            "next": "invalid",
        },
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )


def test_private_thread_members_add_view_returns_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={"thread_id": 1, "slug": "invalid"},
        )
    )
    assert response.status_code == 404


def test_private_thread_members_add_view_checks_private_threads_permission(
    user_client, members_group, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_members_add_view_checks_private_thread_access(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={"thread_id": private_thread.id, "slug": private_thread.slug},
        )
    )
    assert response.status_code == 404


def test_private_thread_members_add_view_checks_private_thread_ownership(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(
        response, "You can&#x27;t add members to this thread.", status_code=403
    )


def test_private_thread_members_add_view_allows_moderators_to_add_new_members(
    moderator_client, other_user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Add members")
