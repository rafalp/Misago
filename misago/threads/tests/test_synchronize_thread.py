from datetime import timedelta

from ...solutions.lock import lock_thread_solution
from ...solutions.select import select_thread_solution
from ...threadevents.create import create_test_thread_update
from ..synchronize import synchronize_thread


def test_synchronize_thread_updates_thread_replies(thread_reply_factory, thread):
    assert thread.replies == 0

    thread_reply_factory(thread)
    thread_reply_factory(thread, is_hidden=True)
    thread_reply_factory(thread, is_unapproved=True)

    synchronize_thread(thread)

    assert thread.replies == 2

    thread.refresh_from_db()
    assert thread.replies == 2


def test_synchronize_thread_sets_has_updates_flag(thread):
    assert not thread.has_updates

    create_test_thread_update(thread, "Actor")

    synchronize_thread(thread)

    assert thread.has_updates

    thread.refresh_from_db()
    assert thread.has_updates


def test_synchronize_thread_removes_has_updates_flag(thread):
    thread.has_updates = True
    thread.save()

    synchronize_thread(thread)

    assert not thread.has_updates

    thread.refresh_from_db()
    assert not thread.has_updates


def test_synchronize_thread_sets_has_poll_flag(poll_factory, thread):
    assert not thread.has_poll

    poll_factory(thread)

    synchronize_thread(thread)

    assert thread.has_poll

    thread.refresh_from_db()
    assert thread.has_poll


def test_synchronize_thread_removes_has_poll_flag(thread):
    thread.has_poll = True
    thread.save()

    synchronize_thread(thread)

    assert not thread.has_poll

    thread.refresh_from_db()
    assert not thread.has_poll


def test_synchronize_thread_sets_has_unapproved_posts_flag(
    thread_reply_factory, thread
):
    assert not thread.has_unapproved_posts

    thread_reply_factory(thread, is_unapproved=True)

    synchronize_thread(thread)

    assert thread.has_unapproved_posts

    thread.refresh_from_db()
    assert thread.has_unapproved_posts


def test_synchronize_thread_removes_has_unapproved_posts_flag(thread):
    thread.has_unapproved_posts = True
    thread.save()

    synchronize_thread(thread)

    assert not thread.has_unapproved_posts

    thread.refresh_from_db()
    assert not thread.has_unapproved_posts


def test_synchronize_thread_sets_has_hidden_posts_flag(thread_reply_factory, thread):
    assert not thread.has_hidden_posts

    thread_reply_factory(thread, is_hidden=True)

    synchronize_thread(thread)

    assert thread.has_hidden_posts

    thread.refresh_from_db()
    assert thread.has_hidden_posts


def test_synchronize_thread_removes_has_hidden_posts_flag(thread):
    thread.has_hidden_posts = True
    thread.save()

    synchronize_thread(thread)

    assert not thread.has_hidden_posts

    thread.refresh_from_db()
    assert not thread.has_hidden_posts


def test_synchronize_thread_updates_first_post_by_user(
    thread_reply_factory, thread, user
):
    first_post = thread.first_post

    first_post.posted_at -= timedelta(minutes=5)
    first_post.poster = user
    first_post.poster_name = user.username

    first_post.save()

    thread.first_post = thread_reply_factory(thread)
    thread.save()

    synchronize_thread(thread)

    assert thread.first_post == first_post
    assert thread.started_at == first_post.posted_at
    assert thread.starter == user
    assert thread.starter_name == user.username
    assert thread.starter_slug == user.slug

    thread.refresh_from_db()
    assert thread.first_post == first_post
    assert thread.started_at == first_post.posted_at
    assert thread.starter == user
    assert thread.starter_name == user.username
    assert thread.starter_slug == user.slug


def test_synchronize_thread_updates_first_post_by_anonymous_user(
    thread_reply_factory, user_thread
):
    first_post = user_thread.first_post

    first_post.posted_at -= timedelta(minutes=5)
    first_post.poster = None
    first_post.poster_name = "Anon"

    first_post.save()

    user_thread.first_post = thread_reply_factory(user_thread)
    user_thread.save()

    synchronize_thread(user_thread)

    assert user_thread.first_post == first_post
    assert user_thread.started_at == first_post.posted_at
    assert user_thread.starter is None
    assert user_thread.starter_name == "Anon"
    assert user_thread.starter_slug == "anon"

    user_thread.refresh_from_db()
    assert user_thread.first_post == first_post
    assert user_thread.started_at == first_post.posted_at
    assert user_thread.starter is None
    assert user_thread.starter_name == "Anon"
    assert user_thread.starter_slug == "anon"


def test_synchronize_thread_updates_last_post_by_user(post_factory, thread, user):
    last_post = post_factory(thread, poster=user)

    synchronize_thread(thread)

    assert thread.last_post == last_post
    assert thread.last_posted_at == last_post.posted_at
    assert thread.last_poster == user
    assert thread.last_poster_name == user.username
    assert thread.last_poster_slug == user.slug

    thread.refresh_from_db()
    assert thread.last_post == last_post
    assert thread.last_posted_at == last_post.posted_at
    assert thread.last_poster == user
    assert thread.last_poster_name == user.username
    assert thread.last_poster_slug == user.slug


def test_synchronize_thread_updates_last_post_by_anonymous_user(
    post_factory, user_thread
):
    last_post = post_factory(user_thread)

    synchronize_thread(user_thread)

    assert user_thread.last_post == last_post
    assert user_thread.last_posted_at == last_post.posted_at
    assert user_thread.last_poster is None
    assert user_thread.last_poster_name == "Poster"
    assert user_thread.last_poster_slug == "poster"

    user_thread.refresh_from_db()
    assert user_thread.last_post == last_post
    assert user_thread.last_posted_at == last_post.posted_at
    assert user_thread.last_poster is None
    assert user_thread.last_poster_name == "Poster"
    assert user_thread.last_poster_slug == "poster"


def test_synchronize_thread_keeps_current_solution(
    post_factory, user_thread, other_user, moderator
):
    solution = post_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, moderator)
    lock_thread_solution(user_thread, moderator)

    synchronize_thread(user_thread)

    assert user_thread.solution == solution
    assert user_thread.solution_posted_at == solution.posted_at
    assert user_thread.solution_by == other_user
    assert user_thread.solution_by_name == other_user.username
    assert user_thread.solution_by_slug == other_user.slug
    assert user_thread.solution_selected_at
    assert user_thread.solution_selected_by == moderator
    assert user_thread.solution_selected_by_name == moderator.username
    assert user_thread.solution_selected_by_slug == moderator.slug
    assert user_thread.solution_is_locked
    assert user_thread.solution_locked_at
    assert user_thread.solution_locked_by == moderator
    assert user_thread.solution_locked_by_name == moderator.username
    assert user_thread.solution_locked_by_slug == moderator.slug

    user_thread.refresh_from_db()
    assert user_thread.solution == solution
    assert user_thread.solution_posted_at == solution.posted_at
    assert user_thread.solution_by == other_user
    assert user_thread.solution_by_name == other_user.username
    assert user_thread.solution_by_slug == other_user.slug
    assert user_thread.solution_selected_at
    assert user_thread.solution_selected_by == moderator
    assert user_thread.solution_selected_by_name == moderator.username
    assert user_thread.solution_selected_by_slug == moderator.slug
    assert user_thread.solution_is_locked
    assert user_thread.solution_locked_at
    assert user_thread.solution_locked_by == moderator
    assert user_thread.solution_locked_by_name == moderator.username
    assert user_thread.solution_locked_by_slug == moderator.slug


def test_synchronize_thread_clears_deleted_solution(
    post_factory, user_thread, other_user, moderator
):
    solution = post_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, moderator)
    lock_thread_solution(user_thread, moderator)

    user_thread.solution = None
    user_thread.save()

    synchronize_thread(user_thread)

    assert user_thread.solution is None
    assert user_thread.solution_posted_at is None
    assert user_thread.solution_by is None
    assert user_thread.solution_by_name is None
    assert user_thread.solution_by_slug is None
    assert user_thread.solution_selected_at is None
    assert user_thread.solution_selected_by is None
    assert user_thread.solution_selected_by_name is None
    assert user_thread.solution_selected_by_slug is None
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None

    user_thread.refresh_from_db()
    assert user_thread.solution is None
    assert user_thread.solution_posted_at is None
    assert user_thread.solution_by is None
    assert user_thread.solution_by_name is None
    assert user_thread.solution_by_slug is None
    assert user_thread.solution_selected_at is None
    assert user_thread.solution_selected_by is None
    assert user_thread.solution_selected_by_name is None
    assert user_thread.solution_selected_by_slug is None
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None


def test_synchronize_thread_clears_moved_solution(
    post_factory, user_thread, other_thread, other_user, moderator
):
    solution = post_factory(other_thread, poster=other_user)
    select_thread_solution(user_thread, solution, moderator)
    lock_thread_solution(user_thread, moderator)

    synchronize_thread(user_thread)

    assert user_thread.solution is None
    assert user_thread.solution_posted_at is None
    assert user_thread.solution_by is None
    assert user_thread.solution_by_name is None
    assert user_thread.solution_by_slug is None
    assert user_thread.solution_selected_at is None
    assert user_thread.solution_selected_by is None
    assert user_thread.solution_selected_by_name is None
    assert user_thread.solution_selected_by_slug is None
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None

    user_thread.refresh_from_db()
    assert user_thread.solution is None
    assert user_thread.solution_posted_at is None
    assert user_thread.solution_by is None
    assert user_thread.solution_by_name is None
    assert user_thread.solution_by_slug is None
    assert user_thread.solution_selected_at is None
    assert user_thread.solution_selected_by is None
    assert user_thread.solution_selected_by_name is None
    assert user_thread.solution_selected_by_slug is None
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None
