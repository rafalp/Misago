import pytest

from ..posts import (
    get_fake_hidden_post,
    get_fake_post,
    get_fake_post_content,
    get_fake_unapproved_post,
)
from ..threads import get_fake_thread


@pytest.fixture
def thread(fake, default_category):
    return get_fake_thread(fake, default_category)


def test_fake_post_can_be_created(fake, thread):
    assert get_fake_post(fake, thread)


def test_fake_post_belongs_to_same_category_as_its_thread(fake, thread):
    post = get_fake_post(fake, thread)
    assert post.category == thread.category


def test_fake_post_is_created_with_guest_poster(fake, thread):
    post = get_fake_post(fake, thread)
    assert post.poster is None


def test_fake_post_is_created_with_guest_poster_has_poster_name(fake, thread):
    post = get_fake_post(fake, thread)
    assert post.poster_name


def test_fake_post_is_created_with_specified_poster(fake, thread, user):
    post = get_fake_post(fake, thread, user)
    assert post.poster == user
    assert post.poster_name == user.username


def test_fake_post_is_created_with_valid_checksum(fake, thread):
    post = get_fake_post(fake, thread)
    assert post.is_valid


def test_fake_post_is_created_with_different_content_every_time(fake, thread):
    post_a = get_fake_post(fake, thread)
    post_b = get_fake_post(fake, thread)
    assert post_a.original != post_b.original
    assert post_a.parsed != post_b.parsed


def test_fake_hidden_post_can_be_created(fake, thread):
    post = get_fake_hidden_post(fake, thread)
    assert post.is_hidden


def test_fake_unapproved_post_can_be_created(fake, thread):
    post = get_fake_unapproved_post(fake, thread)
    assert post.is_unapproved


def test_fake_post_content_can_be_created(fake):
    original, parsed = get_fake_post_content(fake)
    assert original
    assert parsed


def test_different_fake_post_content_is_created_every_time(fake):
    original_a, parsed_a = get_fake_post_content(fake)
    original_b, parsed_b = get_fake_post_content(fake)
    assert original_a != original_b
    assert parsed_a != parsed_b
