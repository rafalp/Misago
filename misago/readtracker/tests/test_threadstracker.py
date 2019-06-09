from datetime import timedelta

from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...threads.test import reply_thread
from ..threadstracker import make_read_aware


def remove_tracking(thread):
    thread.started_on = timezone.now() - timedelta(days=4)
    thread.save()
    thread.first_post.posted_on = thread.started_on
    thread.first_post.save()


def test_falsy_value_can_be_made_read_aware(request_mock):
    make_read_aware(request_mock, None)
    make_read_aware(request_mock, False)


def test_empty_list_can_be_made_read_aware(request_mock):
    make_read_aware(request_mock, [])


def test_read_thread_is_marked_as_read(request_mock, read_thread):
    make_read_aware(request_mock, read_thread)
    assert read_thread.is_read
    assert not read_thread.is_new


def test_read_thread_with_hidden_post_marked_as_unread(request_mock, read_thread):
    reply_thread(read_thread, is_hidden=True)
    make_read_aware(request_mock, read_thread)
    assert not read_thread.is_read
    assert read_thread.is_new


def test_read_thread_with_invisible_post_marked_as_read(request_mock, read_thread):
    reply_thread(read_thread, is_unapproved=True)
    make_read_aware(request_mock, read_thread)
    assert read_thread.is_read
    assert not read_thread.is_new


def test_read_thread_with_unread_post_marked_as_unread(request_mock, read_thread):
    reply_thread(read_thread)
    make_read_aware(request_mock, read_thread)
    assert not read_thread.is_read
    assert read_thread.is_new


def test_untracked_thread_with_tracked_post_is_marked_as_unread(request_mock, thread):
    remove_tracking(thread)
    reply_thread(thread)
    make_read_aware(request_mock, thread)
    assert not thread.is_read
    assert thread.is_new


def test_tracked_thread_is_marked_as_unread(request_mock, thread):
    make_read_aware(request_mock, thread)
    assert not thread.is_read
    assert thread.is_new


def test_thread_with_post_older_than_user_is_marked_as_read(request_mock, thread, user):
    remove_tracking(thread)
    make_read_aware(request_mock, thread)
    assert thread.is_read
    assert not thread.is_new


@override_dynamic_settings(readtracker_cutoff=3)
def test_non_tracked_thread_is_marked_as_read(request_mock, thread, user):
    user.joined_on = timezone.now() - timedelta(days=10)
    user.save()

    remove_tracking(thread)
    make_read_aware(request_mock, thread)
    assert thread.is_read
    assert not thread.is_new


def test_read_thread_with_new_event_is_marked_as_unread(request_mock, read_thread):
    reply_thread(read_thread, is_event=True)
    make_read_aware(request_mock, read_thread)
    assert not read_thread.is_read
    assert read_thread.is_new


def test_read_thread_with_hidden_event_is_marked_as_read(request_mock, read_thread):
    reply_thread(read_thread, is_hidden=True, is_event=True)
    make_read_aware(request_mock, read_thread)
    assert read_thread.is_read
    assert not read_thread.is_new


def test_read_thread_with_hidden_event_visible_to_user_is_marked_as_unread(
    request_mock, read_thread, default_category
):
    request_mock.user_acl["categories"][default_category.id]["can_hide_events"] = 1
    reply_thread(read_thread, is_hidden=True, is_event=True)
    make_read_aware(request_mock, read_thread)
    assert not read_thread.is_read
    assert read_thread.is_new


def test_tracked_thread_is_marked_as_read_for_anonymous_user(
    anonymous_request_mock, thread
):
    make_read_aware(anonymous_request_mock, thread)
    assert thread.is_read
    assert not thread.is_new


@override_dynamic_settings(readtracker_cutoff=3)
def test_non_tracked_thread_is_marked_as_read_for_anonymous_user(
    anonymous_request_mock, thread
):
    remove_tracking(thread)
    make_read_aware(anonymous_request_mock, thread)
    assert thread.is_read
    assert not thread.is_new
