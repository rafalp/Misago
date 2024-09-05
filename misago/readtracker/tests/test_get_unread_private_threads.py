from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...categories.proxy import CategoriesProxy
from ...permissions.proxy import UserPermissionsProxy
from ...threads.models import ThreadParticipant
from ...threads.test import post_thread, reply_thread
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
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(user=user, thread=thread)

    private_threads_category.last_post_on = thread.last_post_on
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
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(
        private_threads_category, started_on=timezone.now().replace(year=2012)
    )
    ThreadParticipant.objects.create(user=user, thread=thread)

    private_threads_category.last_post_on = thread.last_post_on
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
    dynamic_settings, cache_versions, user, private_threads_category
):
    thread = post_thread(
        private_threads_category, started_on=timezone.now() - timedelta(minutes=30)
    )
    ThreadParticipant.objects.create(user=user, thread=thread)

    private_threads_category.last_post_on = thread.last_post_on
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
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(user=user, thread=thread)

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=thread,
        read_time=thread.last_post_on,
    )

    private_threads_category.last_post_on = thread.last_post_on
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
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(user=user, thread=thread)

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=thread,
        read_time=thread.last_post_on,
    )

    reply_thread(thread)

    private_threads_category.last_post_on = thread.last_post_on
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
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(user=user, thread=thread)

    private_threads_category.last_post_on = thread.last_post_on
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
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(user=user, thread=thread)

    reply = reply_thread(thread)

    private_threads_category.last_post_on = thread.last_post_on
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
            request, private_threads_category, reply.posted_on - timedelta(minutes=1)
        )
    ) == [thread]


def test_get_unread_private_threads_excludes_unread_thread_user_is_not_invited_to(
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(private_threads_category)

    private_threads_category.last_post_on = thread.last_post_on
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not get_unread_private_threads(request, private_threads_category, None)
