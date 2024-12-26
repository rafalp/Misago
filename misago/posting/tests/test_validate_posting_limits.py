from datetime import timedelta

from django.core.exceptions import ValidationError

from ...conf.test import override_dynamic_settings
from ..formsets import get_start_thread_formset
from ..state import StartThreadState
from ..validators import validate_posting_limits


def test_validate_posting_limits_passes_user_without_posts(
    user_request, default_category
):
    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)

    assert validate_posting_limits(formset, state)


@override_dynamic_settings(daily_post_limit=5, hourly_post_limit=5)
def test_validate_posting_limits_passes_user_wthin_posts_limits(
    user_request, default_category, user_reply
):
    user_reply.posted_on -= timedelta(hours=1)
    user_reply.save()

    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)

    assert validate_posting_limits(formset, state)


def test_validate_posting_limits_fails_user_on_flood_control(
    user_request, default_category, user_reply
):
    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)

    assert not validate_posting_limits(formset, state)

    error = formset.errors[0]
    assert isinstance(error, ValidationError)
    assert error.message == (
        "You can't post a new message so soon after the previous one."
    )
    assert error.code == "flood_control"


@override_dynamic_settings(flood_control=0, daily_post_limit=1)
def test_validate_posting_limits_fails_user_on_daily_post_limit(
    user_request, default_category, user_reply
):
    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)

    assert not validate_posting_limits(formset, state)

    error = formset.errors[0]
    assert error.message == (
        "You can't post more than %(limit_value)s message within 24 hours."
    )
    assert error.code == "daily_post_limit"
    assert error.params == {"limit_value": 1}


@override_dynamic_settings(flood_control=0, hourly_post_limit=1)
def test_validate_posting_limits_fails_user_on_hourly_post_limit(
    user_request, default_category, user_reply
):
    formset = get_start_thread_formset(user_request, default_category)
    state = StartThreadState(user_request, default_category)

    assert not validate_posting_limits(formset, state)

    error = formset.errors[0]
    assert error.message == (
        "You can't post more than %(limit_value)s message within an hour."
    )
    assert error.code == "hourly_post_limit"
    assert error.params == {"limit_value": 1}
