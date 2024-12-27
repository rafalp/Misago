from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError

from ...conf.test import override_dynamic_settings
from ..floodcontrol import flood_control


def test_flood_control_passes_user_without_posts(user_request):
    flood_control(user_request)


@override_dynamic_settings(flood_control=0)
def test_flood_control_passes_user_if_flood_control_is_disabled(
    user_request, user_reply
):
    flood_control(user_request)


def test_flood_control_fails_user_if_they_have_recent_post(user_request, user_reply):
    with pytest.raises(ValidationError) as exc_info:
        flood_control(user_request)

    assert exc_info.value.message == (
        "You can't post a new message so soon after the previous one."
    )
    assert exc_info.value.code == "flood_control"


def test_flood_control_passes_user_if_their_last_post_is_old(user_request, user_reply):
    user_reply.posted_on -= timedelta(hours=1)
    user_reply.save()

    flood_control(user_request)


def test_flood_control_passes_user_if_they_are_exempt_from_flood_control(
    user_request, user_reply, members_group
):
    members_group.exempt_from_flood_control = True
    members_group.save()

    flood_control(user_request)
