from datetime import timedelta
from unittest.mock import Mock

from ...conf.test import override_dynamic_settings
from ..logging import log_search
from ..throttling import throttle_search


def test_throttle_search_returns_zero_for_user_without_search(dynamic_settings, user):
    request = Mock(settings=dynamic_settings, user=user)
    assert throttle_search(request) == 0


def test_throttle_search_returns_interval_time_for_user_with_recent_search(
    dynamic_settings, user
):
    request = Mock(settings=dynamic_settings, user=user)
    log_search(user, "127.0.0.1", "search query")
    assert throttle_search(request)


def test_throttle_search_returns_zero_for_user_with_old_search(dynamic_settings, user):
    request = Mock(settings=dynamic_settings, user=user)

    search_log = log_search(user, "127.0.0.1", "search query")
    search_log.searched_at -= timedelta(minutes=7)
    search_log.save()

    assert throttle_search(request) == 0


def test_throttle_search_returns_interval_time_for_user_with_old_and_recent_search(
    dynamic_settings, user
):
    request = Mock(settings=dynamic_settings, user=user)

    search_log = log_search(user, "127.0.0.1", "search query")
    search_log.searched_at -= timedelta(minutes=7)
    search_log.save()

    log_search(user, "127.0.0.1", "search query")

    assert throttle_search(request)


@override_dynamic_settings(user_min_search_interval=0)
def test_throttle_search_user_disables_check_if_interval_is_disabled(
    django_assert_num_queries, dynamic_settings, user
):
    request = Mock(settings=dynamic_settings, user=user)

    log_search(user, "127.0.0.1", "search query")

    with django_assert_num_queries(0):
        assert throttle_search(request) == 0


def test_throttle_search_for_user_ignores_other_users(
    dynamic_settings, user, other_user
):
    request = Mock(settings=dynamic_settings, user=user)

    log_search(other_user, "127.0.0.1", "search query")
    log_search(None, "127.0.0.1", "search query")

    assert throttle_search(request) == 0


def test_throttle_search_returns_zero_for_anonymous_user_without_search(
    dynamic_settings, anonymous_user
):
    request = Mock(
        settings=dynamic_settings,
        user=anonymous_user,
        user_ip="127.0.0.1",
    )

    assert throttle_search(request) == 0


def test_throttle_search_returns_interval_time_for_anonymous_user_with_recent_search(
    dynamic_settings, anonymous_user
):
    request = Mock(
        settings=dynamic_settings,
        user=anonymous_user,
        user_ip="127.0.0.1",
    )

    log_search(None, "127.0.0.1", "search query")

    assert throttle_search(request)


def test_throttle_search_returns_zero_for_anonymous_user_with_old_search(
    dynamic_settings, anonymous_user
):
    request = Mock(
        settings=dynamic_settings,
        user=anonymous_user,
        user_ip="127.0.0.1",
    )

    search_log = log_search(None, "127.0.0.1", "search query")
    search_log.searched_at -= timedelta(minutes=7)
    search_log.save()

    assert throttle_search(request) == 0


def test_throttle_search_returns_interval_time_for_anonymous_user_with_old_and_recent_search(
    dynamic_settings, anonymous_user
):
    request = Mock(
        settings=dynamic_settings,
        user=anonymous_user,
        user_ip="127.0.0.1",
    )

    search_log = log_search(None, "127.0.0.1", "search query")
    search_log.searched_at -= timedelta(minutes=7)
    search_log.save()

    log_search(None, "127.0.0.1", "search query")

    assert throttle_search(request)


@override_dynamic_settings(guest_min_search_interval=0)
def test_throttle_search_for_anonymous_user_disables_check_if_interval_is_disabled(
    django_assert_num_queries, dynamic_settings, anonymous_user
):
    request = Mock(
        settings=dynamic_settings,
        user=anonymous_user,
        user_ip="127.0.0.1",
    )

    log_search(None, "127.0.0.1", "search query")

    with django_assert_num_queries(0):
        assert throttle_search(request) == 0


def test_throttle_search_for_anonymous_user_ignores_other_users(
    dynamic_settings, other_user, anonymous_user
):
    request = Mock(
        settings=dynamic_settings,
        user=anonymous_user,
        user_ip="127.0.0.1",
    )

    log_search(other_user, "127.0.0.1", "search query")
    log_search(None, "90.0.0.1", "search query")

    assert throttle_search(request) == 0
