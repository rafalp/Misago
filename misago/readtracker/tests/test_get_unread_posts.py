from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone

from ..models import ReadCategory, ReadThread
from ..tracker import annotate_threads_read_time, get_unread_posts


def test_get_unread_posts_returns_empty_set_for_anonymous_user(
    dynamic_settings, default_category, thread, post, anonymous_user
):
    request = Mock(settings=dynamic_settings, user=anonymous_user)
    queryset = annotate_threads_read_time(anonymous_user, default_category.thread_set)
    unread_posts = get_unread_posts(request, queryset.first(), [post])

    assert not unread_posts


def test_get_unread_posts_includes_unread_post(
    dynamic_settings, default_category, thread, post, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_posts = get_unread_posts(request, queryset.first(), [post])

    assert post.id in unread_posts


def test_get_unread_posts_excludes_unread_post_older_than_user(
    dynamic_settings, default_category, thread, post, user
):
    post.posted_on -= timedelta(minutes=30)
    post.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_posts = get_unread_posts(request, queryset.first(), [post])

    assert not unread_posts


def test_get_unread_posts_excludes_old_unread_post(
    dynamic_settings, default_category, thread, post, user
):
    user.joined_on = user.joined_on.replace(year=2010)
    user.save()

    post.posted_on = post.posted_on.replace(year=2012)
    post.save()

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_posts = get_unread_posts(request, queryset.first(), [post])

    assert not unread_posts


def test_get_unread_posts_excludes_read_post(
    dynamic_settings, default_category, thread, post, user
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
    unread_posts = get_unread_posts(request, queryset.first(), [post])

    assert not unread_posts


def test_get_unread_posts_excludes_unread_post_in_read_category(
    dynamic_settings, default_category, thread, post, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now(),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_posts = get_unread_posts(request, queryset.first(), [post])

    assert not unread_posts


def test_get_unread_posts_includes_read_thread_unread_reply(
    dynamic_settings, default_category, thread, post, reply, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    post.posted_on = timezone.now() - timedelta(minutes=10)
    post.save()

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=thread,
        read_time=timezone.now() - timedelta(minutes=5),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_posts = get_unread_posts(request, queryset.first(), [reply])

    assert post.id not in unread_posts
    assert reply.id in unread_posts


def test_get_unread_posts_includes_read_thread_in_read_category_with_unread_reply(
    dynamic_settings, default_category, thread, post, reply, user
):
    user.joined_on -= timedelta(minutes=30)
    user.save()

    post.posted_on = timezone.now() - timedelta(minutes=10)
    post.save()

    ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=timezone.now() - timedelta(minutes=5),
    )

    request = Mock(settings=dynamic_settings, user=user)
    queryset = annotate_threads_read_time(user, default_category.thread_set)
    unread_posts = get_unread_posts(request, queryset.first(), [reply])

    assert post.id not in unread_posts
    assert reply.id in unread_posts
