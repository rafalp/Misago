from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...categories.proxy import CategoriesProxy
from ...permissions.proxy import UserPermissionsProxy
from ..models import ReadThread
from ..threads import is_category_read


def test_is_category_read_returns_true_for_empty_category(
    dynamic_settings, cache_versions, user, default_category
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert is_category_read(request, default_category, None)


def test_is_category_read_returns_false_for_category_with_unread_thread(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(default_category)

    default_category.last_posted_at = thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not is_category_read(request, default_category, None)


def test_is_category_read_returns_true_for_category_with_old_unread_thread(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(
        default_category, started_at=timezone.now().replace(year=2012)
    )

    default_category.last_posted_at = thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert is_category_read(request, default_category, None)


def test_is_category_read_returns_true_for_category_with_unread_thread_older_than_user(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    thread = thread_factory(default_category, started_at=-900)

    default_category.last_posted_at = thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert is_category_read(request, default_category, None)


def test_is_category_read_returns_true_for_category_with_read_thread(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(default_category, started_at=-900)

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    default_category.last_posted_at = thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert is_category_read(request, default_category, None)


def test_is_category_read_returns_false_for_category_with_one_read_and_one_unread_thread(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(default_category, started_at=-900)

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    unread_thread = thread_factory(default_category, started_at=-300)

    default_category.last_posted_at = unread_thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not is_category_read(request, default_category, None)


def test_is_category_read_returns_true_for_category_with_one_read_and_one_invisible_unread_thread(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(default_category, started_at=-900)

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    thread_factory(default_category, is_hidden=True)

    default_category.last_posted_at = thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert is_category_read(request, default_category, None)


def test_is_category_read_returns_true_for_read_category_with_both_read_threads(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread_factory(default_category, started_at=-900)
    recent_thread = thread_factory(default_category)

    default_category.last_posted_at = recent_thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert is_category_read(request, default_category, timezone.now())


def test_is_category_read_returns_false_for_read_category_with_one_read_and_one_unread_thread(
    thread_factory, dynamic_settings, cache_versions, user, default_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread_factory(default_category, started_at=-90)
    unread_thread = thread_factory(default_category)

    default_category.last_posted_at = unread_thread.last_posted_at
    default_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not is_category_read(
        request, default_category, timezone.now() - timedelta(minutes=15)
    )
