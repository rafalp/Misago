from ..models import Category
from ..synchronize import synchronize_category


def assert_category_is_empty(category: Category):
    assert category.last_posted_at is None
    assert category.last_thread is None
    assert category.last_thread_title is None
    assert category.last_thread_slug is None
    assert category.last_poster is None
    assert category.last_poster_name is None
    assert category.last_poster_slug is None


def test_category_set_last_thread_updates_last_thread_data(
    thread_factory, default_category
):
    synchronize_category(default_category)

    new_thread = thread_factory(default_category)
    default_category.set_last_thread(new_thread)

    assert default_category.last_posted_at == new_thread.last_posted_at
    assert default_category.last_thread == new_thread
    assert default_category.last_thread_title == new_thread.title
    assert default_category.last_thread_slug == new_thread.slug
    assert default_category.last_poster == new_thread.last_poster
    assert default_category.last_poster_name == new_thread.last_poster_name
    assert default_category.last_poster_slug == new_thread.last_poster_slug


def test_category_empty_last_thread_empties_last_thread_data(
    thread_factory, default_category
):
    thread_factory(default_category)

    synchronize_category(default_category)
    default_category.empty_last_thread()

    assert_category_is_empty(default_category)
