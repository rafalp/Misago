from unittest.mock import Mock

from ..filters import MyThreadsFilter, UnapprovedThreadsFilter
from ..models import Thread
from ..test import post_thread


def test_filter_as_choice_method_returns_active_filter_choice(anonymous_user):
    filter = MyThreadsFilter(Mock(user=anonymous_user))
    choice = filter.as_choice("/base/url/", True)

    assert choice.name == filter.name
    assert choice.url == f"/base/url/{filter.slug}/"
    assert choice.active
    assert choice.filter is filter


def test_filter_as_choice_method_returns_inactive_filter_choice(anonymous_user):
    filter = MyThreadsFilter(Mock(user=anonymous_user))
    choice = filter.as_choice("/base/url/", False)

    assert choice.name == filter.name
    assert choice.url == f"/base/url/{filter.slug}/"
    assert not choice.active
    assert choice.filter is filter


def test_my_threads_filter_returns_user_started_thread(user, default_category):
    queryset = Thread.objects.all()
    thread = post_thread(default_category, poster=user)

    filter = MyThreadsFilter(Mock(user=user))
    choice = filter.as_choice("/base/url/", False)

    filtered_queryset = choice.filter(queryset)
    assert list(filtered_queryset) == [thread]


def test_my_threads_filter_excludes_other_users_threads(
    user, other_user, default_category
):
    queryset = Thread.objects.all()
    post_thread(default_category, poster=other_user)

    filter = MyThreadsFilter(Mock(user=user))
    choice = filter.as_choice("/base/url/", False)

    filtered_queryset = choice.filter(queryset)
    assert list(filtered_queryset) == []


def test_my_threads_filter_excludes_anonymous_users_threads(user, default_category):
    queryset = Thread.objects.all()
    post_thread(default_category, poster="Anon")

    filter = MyThreadsFilter(Mock(user=user))
    choice = filter.as_choice("/base/url/", False)

    filtered_queryset = choice.filter(queryset)
    assert list(filtered_queryset) == []


def test_my_threads_filter_returns_empty_queryset_if_user_is_anonymous(
    anonymous_user, user, default_category
):
    queryset = Thread.objects.all()
    post_thread(default_category, poster=user)

    filter = MyThreadsFilter(Mock(user=anonymous_user))
    choice = filter.as_choice("/base/url/", False)

    filtered_queryset = choice.filter(queryset)
    assert list(filtered_queryset) == []


def test_unapproved_threads_filter_returns_unapproved_thread(default_category):
    queryset = Thread.objects.all()
    thread = post_thread(default_category, is_unapproved=True)

    filter = UnapprovedThreadsFilter(Mock())
    choice = filter.as_choice("/base/url/", False)

    filtered_queryset = choice.filter(queryset)
    assert list(filtered_queryset) == [thread]


def test_unapproved_threads_filter_returns_thread_with_unapproved_posts(
    default_category,
):
    queryset = Thread.objects.all()

    thread = post_thread(default_category)
    thread.has_unapproved_posts = True
    thread.save()

    filter = UnapprovedThreadsFilter(Mock())
    choice = filter.as_choice("/base/url/", False)

    filtered_queryset = choice.filter(queryset)
    assert list(filtered_queryset) == [thread]


def test_unapproved_threads_filter_excludes_threads_without_unapproved_status(
    default_category,
):
    queryset = Thread.objects.all()

    thread = post_thread(default_category)
    thread.is_unapproved = False
    thread.has_unapproved_posts = False
    thread.save()

    filter = UnapprovedThreadsFilter(Mock())
    choice = filter.as_choice("/base/url/", False)

    filtered_queryset = choice.filter(queryset)
    assert list(filtered_queryset) == []
