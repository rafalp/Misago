from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...categories.proxy import CategoriesProxy
from ...permissions.proxy import UserPermissionsProxy
from ...threads.models import ThreadParticipant
from ...threads.test import post_thread
from ..models import ReadThread
from ..privatethreads import are_private_threads_read


def test_are_private_threads_read_returns_true_for_empty_category(
    dynamic_settings, cache_versions, user, private_threads_category
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert are_private_threads_read(request, private_threads_category, None)


def test_are_private_threads_read_returns_false_for_unread_thread(
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

    assert not are_private_threads_read(request, private_threads_category, None)


def test_are_private_threads_read_returns_true_for_old_unread_thread(
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

    assert are_private_threads_read(request, private_threads_category, None)


def test_are_private_threads_read_returns_true_for_unread_thread_older_than_user(
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

    assert are_private_threads_read(request, private_threads_category, None)


def test_are_private_threads_read_returns_true_for_read_thread(
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

    assert are_private_threads_read(request, private_threads_category, None)


def test_are_private_threads_read_returns_true_for_one_read_and_one_unread_thread(
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

    unread_thread = post_thread(private_threads_category)

    private_threads_category.last_post_on = unread_thread.last_post_on
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert are_private_threads_read(request, private_threads_category, None)


def test_are_private_threads_read_returns_true_for_one_read_and_one_invisible_unread_thread(
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

    post_thread(private_threads_category)

    private_threads_category.last_post_on = thread.last_post_on
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert are_private_threads_read(request, private_threads_category, None)


def test_are_private_threads_read_returns_true_for_read_both_read_threads(
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    old_thread = post_thread(
        private_threads_category, started_on=timezone.now() - timedelta(minutes=30)
    )
    ThreadParticipant.objects.create(user=user, thread=old_thread)

    recent_thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(user=user, thread=recent_thread)

    private_threads_category.last_post_on = recent_thread.last_post_on
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert are_private_threads_read(request, private_threads_category, timezone.now())


def test_are_private_threads_read_returns_false_for_read_one_read_and_one_unread_thread(
    dynamic_settings, cache_versions, user, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread = post_thread(
        private_threads_category, started_on=timezone.now() - timedelta(minutes=30)
    )
    ThreadParticipant.objects.create(user=user, thread=thread)

    unread_thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(user=user, thread=unread_thread)

    private_threads_category.last_post_on = unread_thread.last_post_on
    private_threads_category.save()

    user_permissions = UserPermissionsProxy(user, cache_versions)
    request = Mock(
        categories=CategoriesProxy(user_permissions, cache_versions),
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )

    assert not are_private_threads_read(
        request, private_threads_category, timezone.now() - timedelta(minutes=15)
    )
