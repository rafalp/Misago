from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError

from ...conf.test import override_dynamic_settings
from ..postlimits import check_daily_post_limit, check_hourly_post_limit


def test_check_daily_post_limit_passes_user_without_posts(user_request):
    check_daily_post_limit(user_request)


def test_check_hourly_post_limit_passes_user_without_posts(user_request):
    check_hourly_post_limit(user_request)


@override_dynamic_settings(daily_post_limit=0)
def test_check_daily_post_limit_passes_user_if_limit_is_removed(
    user_request, user_reply
):
    check_daily_post_limit(user_request)


@override_dynamic_settings(hourly_post_limit=0)
def test_check_hourly_post_limit_passes_user_if_limit_is_removed(
    user_request, user_reply
):
    check_hourly_post_limit(user_request)


@override_dynamic_settings(daily_post_limit=5)
def test_check_daily_post_limit_passes_user_if_they_are_within_limit(
    user_request, user_reply
):
    check_daily_post_limit(user_request)


@override_dynamic_settings(hourly_post_limit=5)
def test_check_hourly_post_limit_passes_user_if_they_are_within_limit(
    user_request, user_reply
):
    check_hourly_post_limit(user_request)


@override_dynamic_settings(daily_post_limit=1)
def test_check_daily_post_limit_fails_user_if_they_have_too_many_posts(
    user_request, user_reply
):
    with pytest.raises(ValidationError) as exc_info:
        check_daily_post_limit(user_request)

    assert exc_info.value.message == (
        "You can't post more than %(limit_value)s message within 24 hours."
    )
    assert exc_info.value.code == "daily_post_limit"
    assert exc_info.value.params == {"limit_value": 1}


@override_dynamic_settings(hourly_post_limit=1)
def test_check_hourly_post_limit_fails_user_if_they_have_too_many_posts(
    user_request, user_reply
):
    with pytest.raises(ValidationError) as exc_info:
        check_hourly_post_limit(user_request)

    assert exc_info.value.message == (
        "You can't post more than %(limit_value)s message within an hour."
    )
    assert exc_info.value.code == "hourly_post_limit"
    assert exc_info.value.params == {"limit_value": 1}


@override_dynamic_settings(daily_post_limit=1)
def test_check_daily_post_limit_excludes_old_posts_from_limit(user_request, user_reply):
    user_reply.posted_on -= timedelta(hours=24)
    user_reply.save()

    check_daily_post_limit(user_request)


@override_dynamic_settings(hourly_post_limit=1)
def test_check_hourly_post_limit_excludes_old_posts_from_limit(
    user_request, user_reply
):
    user_reply.posted_on -= timedelta(hours=1)
    user_reply.save()

    check_hourly_post_limit(user_request)


@override_dynamic_settings(daily_post_limit=1)
def test_check_daily_post_limit_passes_user_if_they_are_exempt_from_posting_limits(
    user_request, user_reply, members_group
):
    members_group.exempt_from_posting_limits = True
    members_group.save()

    check_daily_post_limit(user_request)


@override_dynamic_settings(hourly_post_limit=1)
def test_check_hourly_post_limit_passes_user_if_they_are_exempt_from_posting_limits(
    user_request, user_reply, members_group
):
    members_group.exempt_from_posting_limits = True
    members_group.save()

    check_hourly_post_limit(user_request)
