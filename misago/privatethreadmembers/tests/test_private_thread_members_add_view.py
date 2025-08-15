import pytest
from django.urls import reverse

from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..models import PrivateThreadMember


@pytest.fixture
def mock_notify_on_new_private_thread(mocker):
    return mocker.patch(
        "misago.privatethreadmembers.views.notify_on_new_private_thread"
    )


def test_private_thread_members_add_view_renders_form(user_client, user_private_thread):
    response = user_client.get(
        reverse(
            "misago:private-thread-members-add",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, "Add members")


def test_private_thread_members_add_view_adds_new_thread_members(
    mock_notify_on_new_private_thread, user, user_client, user_private_thread, admin
):
    response = user_client.post(
        reverse(
            "misago:private-thread-members-add",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
        {"users": [admin.username]},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
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
