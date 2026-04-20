from django.utils import timezone

from ..synchronize import synchronize_category


def test_synchronize_category_updates_threads(thread_factory, default_category):
    thread_a = thread_factory(default_category)
    thread_b = thread_factory(default_category)
    thread_c = thread_factory(default_category, is_hidden=True)
    thread_d = thread_factory(default_category, is_unapproved=True)

    synchronize_category(default_category)

    assert default_category.threads == 2
    assert default_category.unapproved_threads == 1


def test_synchronize_category_updates_posts(
    thread_factory, thread_reply_factory, default_category
):
    thread_a = thread_factory(default_category)
    thread_b = thread_factory(default_category)
    thread_c = thread_factory(default_category, is_hidden=True)
    thread_d = thread_factory(default_category, is_unapproved=True)

    thread_reply_factory(thread_a)
    thread_reply_factory(thread_a, is_hidden=True)
    thread_reply_factory(thread_a, is_unapproved=True)
    thread_reply_factory(thread_b)
    thread_reply_factory(thread_b, is_hidden=True)
    thread_reply_factory(thread_b, is_unapproved=True)
    thread_reply_factory(thread_c)
    thread_reply_factory(thread_c, is_hidden=True)
    thread_reply_factory(thread_c, is_unapproved=True)
    thread_reply_factory(thread_d)
    thread_reply_factory(thread_d, is_hidden=True)
    thread_reply_factory(thread_d, is_unapproved=True)

    synchronize_category(default_category)

    assert default_category.posts == 6
    assert default_category.unapproved_posts == 4


def test_synchronize_category_updates_sets_last_thread_by_user(
    thread_factory, user, default_category
):
    thread_a = thread_factory(default_category)
    thread_b = thread_factory(default_category, starter=user)
    thread_c = thread_factory(default_category, is_hidden=True)
    thread_d = thread_factory(default_category, is_unapproved=True)

    synchronize_category(default_category)

    assert default_category.last_posted_at == thread_b.last_posted_at
    assert default_category.last_thread == thread_b
    assert default_category.last_thread_title == thread_b.title
    assert default_category.last_thread_slug == thread_b.slug
    assert default_category.last_poster_id == thread_b.last_poster_id
    assert default_category.last_poster_name == thread_b.last_poster_name
    assert default_category.last_poster_slug == thread_b.last_poster_slug


def test_synchronize_category_updates_sets_last_thread_by_deleted_user(
    thread_factory, default_category
):
    thread_a = thread_factory(default_category)
    thread_b = thread_factory(default_category)
    thread_c = thread_factory(default_category, is_hidden=True)
    thread_d = thread_factory(default_category, is_unapproved=True)

    synchronize_category(default_category)

    assert default_category.last_posted_at == thread_b.last_posted_at
    assert default_category.last_thread == thread_b
    assert default_category.last_thread_title == thread_b.title
    assert default_category.last_thread_slug == thread_b.slug
    assert default_category.last_poster_id is None
    assert default_category.last_poster_name == thread_b.last_poster_name
    assert default_category.last_poster_slug == thread_b.last_poster_slug


def test_synchronize_category_clears_last_thread_in_empty_category(
    user, default_category, user_private_thread
):
    default_category.last_posted_at == user_private_thread.last_posted_at
    default_category.last_thread = user_private_thread
    default_category.last_thread_title = user_private_thread.title
    default_category.last_thread_slug = user_private_thread.slug
    default_category.last_poster = user_private_thread.last_poster
    default_category.last_poster_name = user_private_thread.last_poster_name
    default_category.last_poster_slug = user_private_thread.last_poster_slug
    default_category.save()

    synchronize_category(default_category)

    assert default_category.last_posted_at is None
    assert default_category.last_thread is None
    assert default_category.last_thread_title is None
    assert default_category.last_thread_slug is None
    assert default_category.last_poster_id is None
    assert default_category.last_poster_name is None
    assert default_category.last_poster_slug is None


def test_synchronize_category_clears_last_thread_in_category_without_visible_threads(
    thread_factory, user, default_category
):
    thread_c = thread_factory(default_category, is_hidden=True)
    thread_d = thread_factory(default_category, is_unapproved=True)

    default_category.last_posted_at = thread_d.last_posted_at
    default_category.last_thread = thread_d
    default_category.last_thread_title = thread_d.title
    default_category.last_thread_slug = thread_d.slug
    default_category.last_poster = thread_d.last_poster
    default_category.last_poster_name = thread_d.last_poster_name
    default_category.last_poster_slug = thread_d.last_poster_slug
    default_category.save()

    synchronize_category(default_category)

    assert default_category.last_posted_at is None
    assert default_category.last_thread is None
    assert default_category.last_thread_title is None
    assert default_category.last_thread_slug is None
    assert default_category.last_poster_id is None
    assert default_category.last_poster_name is None
    assert default_category.last_poster_slug is None
