from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ...categories.proxy import CategoriesProxy
from ...permissions.proxy import UserPermissionsProxy
from ...threads.models import ThreadParticipant
from ...threads.test import post_thread
from ..models import ReadThread
from ..privatethreads import unread_private_threads_exist


def test_unread_private_threads_exist_returns_true_for_unread_thread(
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

    assert unread_private_threads_exist(request, private_threads_category, None)


def test_unread_private_threads_exist_returns_false_for_read_thread(
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

    assert not unread_private_threads_exist(request, private_threads_category, None)


def test_unread_private_threads_exist_returns_false_for_thread_in_read_category(
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

    assert not unread_private_threads_exist(
        request, private_threads_category, timezone.now()
    )
