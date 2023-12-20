from datetime import timedelta

import pytest
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...threads.test import reply_thread
from ..categories import get_categories_new_posts
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


def test_get_categories_new_posts_returns_empty_dict_for_empty_list(request_mock):
    assert get_categories_new_posts(request_mock, []) == {}


def test_get_categories_new_posts_returns_false_for_empty_category(
    request_mock, default_category
):
    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_true_for_new_post(
    request_mock, post, default_category
):
    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: True}


def test_get_categories_new_posts_returns_false_for_post_older_than_user(
    request_mock, post, default_category
):
    post.posted_on = timezone.now() - timedelta(days=1)
    post.save()

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


@override_dynamic_settings(readtracker_cutoff=3)
def test_get_categories_new_posts_returns_false_for_post_older_than_cutoff(
    request_mock, user, post, default_category
):
    user.joined_on = timezone.now() - timedelta(days=5)
    user.save()

    post.posted_on = timezone.now() - timedelta(days=4)
    post.save()

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_false_for_read_post(
    request_mock, user, post, default_category
):
    save_read(user, post)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_true_for_new_post_in_untracked_thread(
    request_mock, thread, default_category
):
    remove_tracking(thread)
    reply_thread(thread)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: True}


def test_get_categories_new_posts_returns_false_for_new_post_in_hidden_thread(
    request_mock, hidden_thread, default_category
):
    reply_thread(hidden_thread)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_false_for_read_post_in_untracked_thread(
    request_mock, user, thread, default_category
):
    remove_tracking(thread)
    post = reply_thread(thread)
    save_read(user, post)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_false_for_read_post_in_read_thread(
    request_mock, user, read_thread, default_category
):
    post = reply_thread(read_thread)
    save_read(user, post)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_false_for_unapproved_post_in_read_thread(
    request_mock, user, read_thread, default_category
):
    reply_thread(read_thread, is_unapproved=True)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_true_for_new_event_in_read_thread(
    request_mock, read_thread, default_category
):
    reply_thread(read_thread, is_event=True)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: True}


def test_get_categories_new_posts_returns_false_for_hidden_event_in_read_thread(
    request_mock, read_thread, default_category
):
    reply_thread(read_thread, is_hidden=True, is_event=True)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_true_for_visible_hidden_event_in_read_thread(
    request_mock, read_thread, default_category
):
    request_mock.user_acl["categories"][default_category.id]["can_hide_events"] = 1
    reply_thread(read_thread, is_hidden=True, is_event=True)

    categories_new_posts = get_categories_new_posts(request_mock, [default_category])
    assert categories_new_posts == {default_category.pk: True}


def test_get_categories_new_posts_returns_false_for_empty_category_for_anonymous_user(
    anonymous_request_mock, default_category
):
    categories_new_posts = get_categories_new_posts(
        anonymous_request_mock, [default_category]
    )
    assert categories_new_posts == {default_category.pk: False}


def test_get_categories_new_posts_returns_false_for_tracked_thread_for_anonymous_user(
    anonymous_request_mock, thread, default_category
):
    categories_new_posts = get_categories_new_posts(
        anonymous_request_mock, [default_category]
    )
    assert categories_new_posts == {default_category.pk: False}


@override_dynamic_settings(readtracker_cutoff=3)
def test_get_categories_new_posts_returns_false_for_untracked_thread_for_anonymous_user(
    anonymous_request_mock, thread, default_category
):
    remove_tracking(thread)

    categories_new_posts = get_categories_new_posts(
        anonymous_request_mock, [default_category]
    )
    assert categories_new_posts == {default_category.pk: False}
