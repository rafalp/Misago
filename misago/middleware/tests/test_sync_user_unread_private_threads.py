from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...categories.proxy import CategoriesProxy
from ...permissions.proxy import UserPermissionsProxy
from ...threads.models import ThreadParticipant
from ...threads.test import post_thread
from ...readtracker.models import ReadThread
from ..privatethreads import sync_user_unread_private_threads


def test_sync_user_unread_private_threads_middleware_updates_user_with_unread_threads(
    dynamic_settings, cache_versions, user, user_private_thread
):
    user.unread_private_threads = 0
    user.sync_unread_private_threads = True
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    middleware = sync_user_unread_private_threads(Mock())
    middleware(request)

    user.refresh_from_db()
    assert user.unread_private_threads == 1
    assert not user.sync_unread_private_threads


def test_sync_user_unread_private_threads_middleware_updates_user_without_unread_threads(
    dynamic_settings, cache_versions, user
):
    user.unread_private_threads = 100
    user.sync_unread_private_threads = True
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    middleware = sync_user_unread_private_threads(Mock())
    middleware(request)

    user.refresh_from_db()
    assert user.unread_private_threads == 0
    assert not user.sync_unread_private_threads


def test_sync_user_unread_private_threads_middleware_skips_anonymous_user(
    dynamic_settings, cache_versions, anonymous_user
):
    user_permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=anonymous_user,
        user_permissions=user_permissions,
    )

    middleware = sync_user_unread_private_threads(Mock())
    middleware(request)


def test_sync_user_unread_private_threads_middleware_skips_user_without_sync_flag(
    dynamic_settings, cache_versions, user
):
    user.unread_private_threads = 100
    user.sync_unread_private_threads = False
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    middleware = sync_user_unread_private_threads(Mock())
    middleware(request)

    user.refresh_from_db()
    assert user.unread_private_threads == 100
    assert not user.sync_unread_private_threads
