from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...categories.proxy import CategoriesProxy
from ...permissions.proxy import UserPermissionsProxy
from ...privatethreads.models import PrivateThreadMember
from ..models import ReadThread
from ..privatethreads import get_unread_private_threads


def test_get_unread_private_threads_returns_nothing_for_empty_category(
    dynamic_settings, cache_versions, user, private_threads_category
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not get_unread_private_threads(request, private_threads_category, None)


def test_get_unread_private_threads_returns_unread_thread(
    thread_factory, dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(user=user, thread=thread)

    private_threads_category.last_posted_at = thread.last_posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert list(
        get_unread_private_threads(request, private_threads_category, None)
    ) == [thread]


def test_get_unread_private_threads_excludes_unread_thread_older_than_tracking_period(
    thread_factory, dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(
        private_threads_category, started_at=timezone.now().replace(year=2012)
    )
    PrivateThreadMember.objects.create(user=user, thread=thread)

    private_threads_category.last_posted_at = thread.last_posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not get_unread_private_threads(request, private_threads_category, None)


def test_get_unread_private_threads_excludes_unread_thread_older_than_user(
    thread_factory, dynamic_settings, cache_versions, user, private_threads_category
):
    thread = thread_factory(private_threads_category, started_at=-900)
    PrivateThreadMember.objects.create(user=user, thread=thread)

    private_threads_category.last_posted_at = thread.last_posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not get_unread_private_threads(request, private_threads_category, None)


def test_get_unread_private_threads_excludes_read_thread(
    thread_factory, dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(private_threads_category, started_at=-900)
    PrivateThreadMember.objects.create(user=user, thread=thread)

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    private_threads_category.last_posted_at = thread.last_posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not get_unread_private_threads(request, private_threads_category, None)


def test_get_unread_private_threads_includes_read_thread_with_unread_reply(
    thread_factory,
    thread_reply_factory,
    dynamic_settings,
    cache_versions,
    user,
    private_threads_category,
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(private_threads_category, started_at=-3600)
    PrivateThreadMember.objects.create(user=user, thread=thread)

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    reply = thread_reply_factory(thread)

    private_threads_category.last_posted_at = reply.posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert list(
        get_unread_private_threads(request, private_threads_category, None)
    ) == [thread]


def test_get_unread_private_threads_excludes_thread_in_read_category(
    thread_factory, dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(private_threads_category, started_at=-3600)
    PrivateThreadMember.objects.create(user=user, thread=thread)

    private_threads_category.last_posted_at = thread.last_posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not get_unread_private_threads(
        request, private_threads_category, timezone.now()
    )


def test_get_unread_private_threads_includes_thread_in_read_category_with_unread_reply(
    thread_factory,
    thread_reply_factory,
    dynamic_settings,
    cache_versions,
    user,
    private_threads_category,
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(private_threads_category, started_at=-3600)
    PrivateThreadMember.objects.create(user=user, thread=thread)

    reply = thread_reply_factory(thread)

    private_threads_category.last_posted_at = reply.posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert list(
        get_unread_private_threads(
            request, private_threads_category, reply.posted_at - timedelta(minutes=1)
        )
    ) == [thread]


def test_get_unread_private_threads_excludes_unread_thread_user_is_not_invited_to(
    thread_factory, dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = thread_factory(private_threads_category)

    private_threads_category.last_posted_at = thread.last_posted_at
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not get_unread_private_threads(request, private_threads_category, None)
