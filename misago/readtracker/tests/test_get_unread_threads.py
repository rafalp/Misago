from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ..models import ReadCategory, ReadThread
from ..tracker import (
    get_unread_threads,
    threads_annotate_user_readcategory_time,
    threads_select_related_user_readthread,
)


def test_get_unread_threads_returns_empty_set_for_anonymous_user(
    dynamic_settings, default_category, thread, anonymous_user
):
    request = Mock(settings=dynamic_settings, user=anonymous_user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, anonymous_user)
    queryset = threads_annotate_user_readcategory_time(queryset, anonymous_user)

    unread_threads = get_unread_threads(request, queryset.all())
    assert not unread_threads


def test_get_unread_threads_includes_unread_thread(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    request = Mock(settings=dynamic_settings, user=user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, user)
    queryset = threads_annotate_user_readcategory_time(queryset, user)

    unread_threads = get_unread_threads(request, queryset.all())
    assert thread.id in unread_threads


def test_get_unread_threads_excludes_unread_thread_older_than_user(
    dynamic_settings, default_category, thread, user
):
    thread.last_posted_at -= timedelta(minutes=30)
    thread.save()

    request = Mock(settings=dynamic_settings, user=user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, user)
    queryset = threads_annotate_user_readcategory_time(queryset, user)

    unread_threads = get_unread_threads(request, queryset.all())
    assert not unread_threads


def test_get_unread_threads_excludes_old_unread_thread(
    dynamic_settings, default_category, thread, user
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    thread.last_posted_at = thread.last_posted_at.replace(year=2012)
    thread.save()

    request = Mock(settings=dynamic_settings, user=user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, user)
    queryset = threads_annotate_user_readcategory_time(queryset, user)

    unread_threads = get_unread_threads(request, queryset.all())
    assert not unread_threads


def test_get_unread_threads_excludes_read_thread(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    thread.last_posted_at -= timedelta(minutes=10)
    thread.save()

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    request = Mock(settings=dynamic_settings, user=user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, user)
    queryset = threads_annotate_user_readcategory_time(queryset, user)
    unread_threads = get_unread_threads(request, queryset.all())

    assert not unread_threads


def test_get_unread_threads_excludes_unread_thread_in_read_category(
    dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    thread.last_posted_at -= timedelta(minutes=10)
    thread.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=thread.last_posted_at,
    )

    request = Mock(settings=dynamic_settings, user=user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, user)
    queryset = threads_annotate_user_readcategory_time(queryset, user)

    unread_threads = get_unread_threads(request, queryset.all())
    assert not unread_threads


def test_get_unread_threads_includes_read_thread_with_unread_reply(
    thread_reply_factory, dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    thread.last_posted_at -= timedelta(minutes=10)
    thread.save()

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=thread.last_posted_at,
    )

    thread_reply_factory(thread)

    request = Mock(settings=dynamic_settings, user=user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, user)
    queryset = threads_annotate_user_readcategory_time(queryset, user)

    unread_threads = get_unread_threads(request, queryset.all())
    assert thread.id in unread_threads


def test_get_unread_threads_includes_read_thread_in_read_category_with_unread_reply(
    thread_reply_factory, dynamic_settings, default_category, thread, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    thread.last_posted_at -= timedelta(minutes=10)
    thread.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now() - timedelta(minutes=5),
    )

    thread_reply_factory(thread)

    request = Mock(settings=dynamic_settings, user=user)

    queryset = default_category.thread_set
    queryset = threads_select_related_user_readthread(queryset, user)
    queryset = threads_annotate_user_readcategory_time(queryset, user)

    unread_threads = get_unread_threads(request, queryset.all())
    assert thread.id in unread_threads
