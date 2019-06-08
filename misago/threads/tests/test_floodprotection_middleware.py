from datetime import timedelta

import pytest
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..api.postingendpoint import PostingEndpoint, PostingInterrupt
from ..api.postingendpoint.floodprotection import FloodProtectionMiddleware
from ..test import post_thread

default_acl = {"can_omit_flood_protection": False}
can_omit_flood_acl = {"can_omit_flood_protection": True}


def test_middleware_lets_users_first_post_through(dynamic_settings, user):
    user.update_fields = []
    middleware = FloodProtectionMiddleware(
        settings=dynamic_settings, user=user, user_acl=default_acl
    )
    middleware.interrupt_posting(None)


def test_middleware_updates_users_last_post_datetime(dynamic_settings, user):
    user.update_fields = []
    middleware = FloodProtectionMiddleware(
        settings=dynamic_settings, user=user, user_acl=default_acl
    )
    middleware.interrupt_posting(None)
    assert user.last_posted_on
    assert "last_posted_on" in user.update_fields


def test_middleware_interrupts_posting_because_previous_post_was_posted_too_recently(
    dynamic_settings, user
):
    user.last_posted_on = timezone.now()
    user.update_fields = []

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    assert middleware.use_this_middleware()

    with pytest.raises(PostingInterrupt):
        middleware.interrupt_posting(None)


def test_middleware_lets_users_next_post_through_if_previous_post_is_not_recent(
    dynamic_settings, user
):
    user.last_posted_on = timezone.now() - timedelta(seconds=10)
    user.update_fields = []

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    assert middleware.use_this_middleware()
    middleware.interrupt_posting(None)


def test_middleware_is_not_used_if_user_has_permission_to_omit_flood_protection(
    dynamic_settings, user
):
    user.last_posted_on = timezone.now()
    user.update_fields = []

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=can_omit_flood_acl,
    )
    assert not middleware.use_this_middleware()


def test_middleware_is_not_used_if_user_edits_post(dynamic_settings, user):
    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.EDIT,
        settings=dynamic_settings,
        user=user,
        user_acl=can_omit_flood_acl,
    )
    assert not middleware.use_this_middleware()


@override_dynamic_settings(hourly_post_limit=3)
def test_middleware_interrupts_posting_if_hourly_limit_was_met(
    default_category, dynamic_settings, user
):
    user.update_fields = []

    for _ in range(3):
        post_thread(default_category, poster=user)

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    assert middleware.use_this_middleware()

    with pytest.raises(PostingInterrupt):
        middleware.interrupt_posting(None)


@override_dynamic_settings(hourly_post_limit=0)
def test_old_posts_dont_count_to_hourly_limit(default_category, dynamic_settings, user):
    user.update_fields = []

    for _ in range(3):
        post_thread(
            default_category,
            poster=user,
            started_on=timezone.now() - timedelta(hours=1),
        )

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    middleware.interrupt_posting(None)


@override_dynamic_settings(hourly_post_limit=0)
def test_middleware_lets_post_through_if_hourly_limit_was_disabled(
    default_category, dynamic_settings, user
):
    user.update_fields = []

    for _ in range(3):
        post_thread(default_category, poster=user)

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    middleware.interrupt_posting(None)


@override_dynamic_settings(daily_post_limit=3)
def test_middleware_interrupts_posting_if_daily_limit_was_met(
    default_category, dynamic_settings, user
):
    user.update_fields = []

    for _ in range(3):
        post_thread(default_category, poster=user)

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    assert middleware.use_this_middleware()

    with pytest.raises(PostingInterrupt):
        middleware.interrupt_posting(None)


@override_dynamic_settings(daily_post_limit=0)
def test_old_posts_dont_count_to_daily_limit(default_category, dynamic_settings, user):
    user.update_fields = []

    for _ in range(3):
        post_thread(
            default_category, poster=user, started_on=timezone.now() - timedelta(days=1)
        )

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    middleware.interrupt_posting(None)


@override_dynamic_settings(daily_post_limit=0)
def test_middleware_lets_post_through_if_daily_limit_was_disabled(
    default_category, dynamic_settings, user
):
    user.update_fields = []

    for _ in range(3):
        post_thread(default_category, poster=user)

    middleware = FloodProtectionMiddleware(
        mode=PostingEndpoint.START,
        settings=dynamic_settings,
        user=user,
        user_acl=default_acl,
    )
    middleware.interrupt_posting(None)
