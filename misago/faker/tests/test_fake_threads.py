from ..threads import (
    get_fake_closed_thread,
    get_fake_hidden_thread,
    get_fake_thread,
    get_fake_unapproved_thread,
)


def test_fake_thread_can_be_created(fake, default_category):
    assert get_fake_thread(fake, default_category)


def test_fake_thread_is_created_with_opening_post(fake, default_category):
    thread = get_fake_thread(fake, default_category)
    assert thread.first_post


def test_fake_thread_is_created_with_guest_starter(fake, default_category):
    thread = get_fake_thread(fake, default_category)
    assert thread.first_post.poster is None


def test_fake_thread_is_created_with_specified_starter(fake, default_category, user):
    thread = get_fake_thread(fake, default_category, user)
    assert thread.first_post.poster == user
    assert thread.first_post.poster_name == user.username


def test_fake_thread_is_created_in_specified_category(fake, default_category):
    thread = get_fake_thread(fake, default_category)
    assert thread.category == default_category
    assert thread.first_post.category == default_category


def test_fake_closed_thread_can_be_created(fake, default_category):
    thread = get_fake_closed_thread(fake, default_category)
    assert thread.is_closed


def test_fake_hidden_thread_can_be_created(fake, default_category):
    thread = get_fake_hidden_thread(fake, default_category)
    assert thread.is_hidden
    assert thread.first_post.is_hidden


def test_fake_unapproved_thread_can_be_created(fake, default_category):
    thread = get_fake_unapproved_thread(fake, default_category)
    assert thread.is_unapproved
    assert thread.first_post.is_unapproved


def test_different_fake_thread_title_is_used_every_time(fake, default_category):
    thread_a = get_fake_thread(fake, default_category)
    thread_b = get_fake_thread(fake, default_category)
    assert thread_a.title != thread_b.title
