from ...threads.test import post_thread
from ..models import Category


def assert_category_is_empty(category: Category):
    assert category.last_post_on is None
    assert category.last_thread is None
    assert category.last_thread_title is None
    assert category.last_thread_slug is None
    assert category.last_poster is None
    assert category.last_poster_name is None
    assert category.last_poster_slug is None


def test_category_synchronize_updates_category_data(default_category):
    default_category.synchronize()

    assert default_category.threads == 0
    assert default_category.posts == 0

    thread = post_thread(default_category)
    hidden = post_thread(default_category)
    unapproved = post_thread(default_category)

    default_category.synchronize()
    assert default_category.threads == 3
    assert default_category.posts == 3
    assert default_category.last_thread == unapproved

    unapproved.is_unapproved = True
    unapproved.post_set.update(is_unapproved=True)
    unapproved.save()

    default_category.synchronize()
    assert default_category.threads == 2
    assert default_category.posts == 2
    assert default_category.last_thread == hidden

    hidden.is_hidden = True
    hidden.post_set.update(is_hidden=True)
    hidden.save()

    default_category.synchronize()
    assert default_category.threads == 1
    assert default_category.posts == 1
    assert default_category.last_thread == thread

    unapproved.is_unapproved = False
    unapproved.post_set.update(is_unapproved=False)
    unapproved.save()

    default_category.synchronize()
    assert default_category.threads == 2
    assert default_category.posts == 2
    assert default_category.last_thread == unapproved


def test_category_set_last_thread_updates_last_thread_data(default_category):
    default_category.synchronize()

    new_thread = post_thread(default_category)
    default_category.set_last_thread(new_thread)

    assert default_category.last_post_on == new_thread.last_post_on
    assert default_category.last_thread == new_thread
    assert default_category.last_thread_title == new_thread.title
    assert default_category.last_thread_slug == new_thread.slug
    assert default_category.last_poster == new_thread.last_poster
    assert default_category.last_poster_name == new_thread.last_poster_name
    assert default_category.last_poster_slug == new_thread.last_poster_slug


def test_category_empty_last_thread_empties_last_thread_data(default_category):
    post_thread(default_category)

    default_category.synchronize()
    default_category.empty_last_thread()

    assert_category_is_empty(default_category)
