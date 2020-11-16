from datetime import timedelta

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


def test_category_with_new_event_in_read_thread_is_marked_as_unread(
    request_mock, read_thread, default_category
):
    reply_thread(read_thread, is_event=True)
    make_read_aware(request_mock, default_category)
    assert not default_category.is_read
    assert default_category.is_new


def test_category_with_hidden_event_in_read_thread_is_marked_as_read(
    request_mock, read_thread, default_category
):
    reply_thread(read_thread, is_hidden=True, is_event=True)
    make_read_aware(request_mock, default_category)
    assert default_category.is_read
    assert not default_category.is_new


def test_category_with_hidden_event_visible_to_user_in_read_thread_is_marked_as_unread(
    request_mock, read_thread, default_category
):
    request_mock.user_acl["categories"][default_category.id]["can_hide_events"] = 1
    reply_thread(read_thread, is_hidden=True, is_event=True)
    make_read_aware(request_mock, default_category)
    assert not default_category.is_read
    assert default_category.is_new


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
