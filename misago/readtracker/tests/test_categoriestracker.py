from datetime import timedelta
from unittest.mock import Mock

import pytest
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...threads.test import reply_thread
from ..categoriestracker import make_read_aware
from ..poststracker import save_read


def remove_tracking(thread):
    thread.started_on = timezone.now() - timedelta(days=4)
    thread.save()
    thread.first_post.posted_on = thread.started_on
    thread.first_post.save()


@pytest.fixture
def read_thread(user, thread):
    save_read(user, thread.first_post)
    return thread


@pytest.fixture
def request_mock(dynamic_settings, user, user_acl):
    return Mock(settings=dynamic_settings, user=user, user_acl=user_acl)


def test_falsy_value_can_be_made_read_aware(request_mock):
    make_read_aware(request_mock, None)
    make_read_aware(request_mock, False)


def test_empty_list_can_be_made_read_aware(request_mock):
    make_read_aware(request_mock, [])


def test_empty_category_is_marked_as_read(request_mock, default_category):
    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_tracked_post_is_marked_as_read(
    request_mock, post, default_category
):
    make_read_aware(request_mock, default_category)
    assert not default_category.is_read
    assert default_category.is_new


def test_category_with_post_older_than_user_is_marked_as_read(
    request_mock, post, default_category
):
    post.posted_on = timezone.now() - timedelta(days=1)
    post.save()

    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


@override_dynamic_settings(readtracker_cutoff=3)
def test_category_with_post_older_than_cutoff_is_marked_as_read(
    request_mock, user, post, default_category
):
    user.joined_on = timezone.now() - timedelta(days=5)
    user.save()

    post.posted_on = timezone.now() - timedelta(days=4)
    post.save()

    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_read_post_is_marked_as_read(
    request_mock, user, post, default_category
):
    save_read(user, post)
    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_post_in_thread_older_than_user_is_marked_as_unread(
    request_mock, thread, default_category
):
    remove_tracking(thread)
    reply_thread(thread)
    make_read_aware(request_mock, default_category)
    assert not default_category.is_read
    assert default_category.is_new


def test_category_with_post_in_invisible_thread_is_marked_as_read(
    request_mock, hidden_thread, default_category
):
    reply_thread(hidden_thread)
    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_read_post_in_thread_older_than_user_is_marked_as_read(
    request_mock, user, thread, default_category
):
    remove_tracking(thread)
    post = reply_thread(thread)
    save_read(user, post)
    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_read_post_in_read_thread_is_marked_as_read(
    request_mock, user, read_thread, default_category
):
    post = reply_thread(read_thread)
    save_read(user, post)
    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_invisible_post_in_read_thread_is_marked_as_read(
    request_mock, user, read_thread, default_category
):
    reply_thread(read_thread, is_unapproved=True)
    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


@pytest.fixture
def anonymous_request_mock(dynamic_settings, anonymous_user, anonymous_user_acl):
    return Mock(
        settings=dynamic_settings, user=anonymous_user, user_acl=anonymous_user_acl
    )


def test_empty_category_is_marked_as_read_for_anonymous_user(
    anonymous_request_mock, default_category
):
    make_read_aware(anonymous_request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_tracked_thread_is_marked_as_read_for_anonymous_user(
    anonymous_request_mock, thread, default_category
):
    make_read_aware(anonymous_request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


@override_dynamic_settings(readtracker_cutoff=3)
def test_category_with_non_tracked_thread_is_marked_as_read_for_anonymous_user(
    anonymous_request_mock, thread, default_category
):
    remove_tracking(thread)
    make_read_aware(anonymous_request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new
