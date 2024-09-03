from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ..models import ReadCategory, ReadThread
from ..tracker import annotate_threads_read_time, get_unread_threads


def test_get_unread_threads_returns_empty_set_for_anonymous_user(
    dynamic_settings, default_category, thread, anonymous_user
):
    request = Mock(settings=dynamic_settings, user=anonymous_user)
    queryset = annotate_threads_read_time(anonymous_user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert not unread_threads


def test_get_unread_threads_includes_unread_thread(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert thread.id in unread_threads


def test_get_unread_threads_excludes_unread_thread_older_than_user(
    dynamic_settings, default_category, thread, user
):
    thread.last_post_on -= timedelta(minutes=30)
    thread.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert not unread_threads


def test_get_unread_threads_excludes_old_unread_thread(
    dynamic_settings, default_category, thread, user
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread.last_post_on = thread.last_post_on.replace(year=2012)
    thread.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert not unread_threads


def test_get_unread_threads_excludes_read_thread(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=timezone.now(),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert not unread_threads


def test_get_unread_threads_excludes_unread_thread_in_read_category(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=thread.last_post_on,
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert not unread_threads


def test_get_unread_threads_includes_read_thread_with_unread_reply(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=timezone.now() - timedelta(minutes=5),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert thread.id in unread_threads


def test_get_unread_threads_includes_read_thread_in_read_category_with_unread_reply(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now() - timedelta(minutes=5),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_threads = get_unread_threads(request, queryset.all())

    assert thread.id in unread_threads
