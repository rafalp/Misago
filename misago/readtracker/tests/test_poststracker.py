from datetime import timedelta

import pytest
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..poststracker import make_read_aware, save_read


def test_falsy_value_can_be_made_read_aware(request_mock):
    make_read_aware(request_mock, None)
    make_read_aware(request_mock, False)


def test_empty_list_can_be_made_read_aware(request_mock):
    make_read_aware(request_mock, [])


@pytest.fixture
def read_post(user, post):
    save_read(user, post)
    return post


def test_tracked_post_is_marked_as_not_read_and_new(request_mock, post):
    make_read_aware(request_mock, post)
    assert not post.is_read
    assert post.is_new


@override_dynamic_settings(readtracker_cutoff=3)
def test_not_tracked_post_is_marked_as_read_and_not_new(request_mock, post):
    post.posted_on = timezone.now() - timedelta(days=4)
    post.save()

    make_read_aware(request_mock, post)
    assert post.is_read
    assert not post.is_new


def test_tracked_read_post_is_marked_as_read_and_not_new(request_mock, read_post):
    make_read_aware(request_mock, read_post)
    assert read_post.is_read
    assert not read_post.is_new


@override_dynamic_settings(readtracker_cutoff=3)
def test_not_tracked_read_post_is_marked_as_read_and_not_new(request_mock, read_post):
    read_post.posted_on = timezone.now() - timedelta(days=4)
    read_post.save()

    make_read_aware(request_mock, read_post)
    assert read_post.is_read
    assert not read_post.is_new


def test_iterable_of_posts_can_be_made_read_aware(request_mock, post):
    make_read_aware(request_mock, [post])
    assert not post.is_read
    assert post.is_new


def test_tracked_post_read_by_other_user_is_marked_as_not_read_and_new(
    request_mock, other_user, post
):
    save_read(other_user, post)
    make_read_aware(request_mock, post)
    assert not post.is_read
    assert post.is_new


def test_tracked_post_is_marked_as_read_and_not_new_for_anonymous_user(
    anonymous_request_mock, post
):
    make_read_aware(anonymous_request_mock, post)
    assert post.is_read
    assert not post.is_new


@override_dynamic_settings(readtracker_cutoff=3)
def test_not_tracked_post_is_marked_as_read_and_not_new_for_anonymous_user(
    anonymous_request_mock, post
):
    post.posted_on = timezone.now() - timedelta(days=4)
    post.save()

    make_read_aware(anonymous_request_mock, post)
    assert post.is_read
    assert not post.is_new
