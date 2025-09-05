from django.urls import reverse
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...html.element import html_element
from ...permissions.models import Moderator
from ...privatethreadmembers.models import PrivateThreadMember
from ...test import assert_contains, assert_not_contains
from ...threadupdates.create import create_test_thread_update


def test_private_thread_replies_view_shows_thread_members(
    user_client, user_private_thread, user, other_user, moderator
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "3 members")
    assert_contains(response, user.username)
    assert_contains(response, other_user.username)
    assert_contains(response, moderator.username)
