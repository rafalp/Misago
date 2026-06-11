import pytest

from ...categories.synchronize import synchronize_category
from ...polls.models import Poll, PollVote
from ...solutions.thread import select_thread_solution
from ..create import create_thread
from ..merge import get_thread_merge_conflicts, merge_threads
from ..models import Thread


def test_get_thread_merge_conflicts_returns_no_conflicts(thread, user_thread):
    conflicts = get_thread_merge_conflicts([thread, user_thread])
    assert not conflicts


def test_get_thread_merge_conflicts_returns_poll_conflict(
    poll_factory, thread, user_thread, other_user_thread
):
    thread_poll = poll_factory(thread)
    user_thread_poll = poll_factory(user_thread)

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {
        "poll": sorted([thread_poll, user_thread_poll], key=lambda i: i.thread_id),
    }


def test_get_thread_merge_conflicts_returns_single_poll(
    poll_factory, thread, user_thread, other_user_thread
):
    user_thread_poll = poll_factory(user_thread)

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {"poll": [user_thread_poll]}


def test_get_thread_merge_conflicts_returns_solution_conflict(
    thread_reply_factory, thread, user_thread, other_user_thread
):
    thread_solution = thread_reply_factory(thread, poster="DeletedUser")
    user_thread_solution = thread_reply_factory(user_thread, poster="DeletedUser")

    select_thread_solution(thread, thread_solution, "John")
    select_thread_solution(user_thread, user_thread_solution, "Bob")

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {
        "solution": sorted([thread, user_thread], key=lambda i: i.id),
    }


def test_get_thread_merge_conflicts_returns_single_solution(
    thread_reply_factory, thread, user_thread, other_user_thread
):
    user_thread_solution = thread_reply_factory(user_thread, poster="DeletedUser")
    select_thread_solution(user_thread, user_thread_solution, "Bob")

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {
        "solution": [user_thread],
    }


def test_merge_threads_merges_threads_posts(
    sibling_category, thread, user_thread, other_user_thread
):
    thread_post = thread.first_post
    user_thread_post = user_thread.first_post
    other_user_thread_post = other_user_thread.first_post

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    thread_post.refresh_from_db()
    assert thread_post.category == sibling_category
    assert thread_post.thread == new_thread

    user_thread_post.refresh_from_db()
    assert user_thread_post.category == sibling_category
    assert user_thread_post.thread == new_thread

    other_user_thread_post.refresh_from_db()
    assert other_user_thread_post.category == sibling_category
    assert other_user_thread_post.thread == new_thread


def test_merge_threads_merges_threads_solutions(
    thread_reply_factory, sibling_category, thread, user_thread, other_user_thread
):
    thread_solution = thread_reply_factory(thread, poster="PosterA")
    user_thread_solution = thread_reply_factory(thread, poster="PosterB")
    other_user_thread_solution = thread_reply_factory(thread, poster="PosterD")

    select_thread_solution(thread, thread_solution, "John")
    select_thread_solution(user_thread, user_thread_solution, "Bob")
    select_thread_solution(other_user_thread, other_user_thread_solution, "Alice")

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(
        new_thread,
        [thread, user_thread, other_user_thread],
        {"solution": user_thread},
    )

    new_thread.refresh_from_db()
    assert new_thread.solution == user_thread_solution


def test_merge_threads_keeps_new_thread_solution(
    thread_reply_factory, sibling_category, thread, user_thread, other_user_thread
):
    thread_solution = thread_reply_factory(thread, poster="PosterA")
    user_thread_solution = thread_reply_factory(thread, poster="PosterB")
    other_user_thread_solution = thread_reply_factory(thread, poster="PosterD")

    select_thread_solution(thread, thread_solution, "John")
    select_thread_solution(user_thread, user_thread_solution, "Bob")
    select_thread_solution(other_user_thread, other_user_thread_solution, "Alice")

    new_thread = create_thread(sibling_category, "Merged thread")

    new_thread_solution = thread_reply_factory(new_thread, poster="PosterA")
    select_thread_solution(new_thread, new_thread_solution, "Diana")

    merge_threads(
        new_thread,
        [thread, user_thread, other_user_thread],
        {"solution": new_thread},
    )

    new_thread.refresh_from_db()
    assert new_thread.solution == new_thread_solution


def test_merge_threads_merges_poll_with_votes(
    poll_factory,
    poll_vote_factory,
    sibling_category,
    thread,
    user_thread,
    other_user_thread,
):
    thread_poll = poll_factory(thread)
    thread_poll_vote = poll_vote_factory(thread_poll, "OtherUser", "choice2")

    user_thread_poll = poll_factory(user_thread)
    user_thread_poll_vote = poll_vote_factory(user_thread_poll, "OtherUser", "choice2")

    other_user_thread_poll = poll_factory(other_user_thread)
    other_user_thread_poll_vote = poll_vote_factory(
        other_user_thread_poll, "OtherUser", "choice2"
    )

    new_thread = create_thread(sibling_category, "Merged thread")

    merge_threads(
        new_thread,
        [thread, user_thread, other_user_thread],
        {"poll": user_thread_poll},
    )

    user_thread_poll.refresh_from_db()
    assert user_thread_poll.category == sibling_category
    assert user_thread_poll.thread == new_thread

    user_thread_poll_vote.refresh_from_db()
    assert user_thread_poll_vote.category == sibling_category
    assert user_thread_poll_vote.thread == new_thread

    with pytest.raises(Poll.DoesNotExist):
        thread_poll.refresh_from_db()

    with pytest.raises(PollVote.DoesNotExist):
        thread_poll_vote.refresh_from_db()

    with pytest.raises(Poll.DoesNotExist):
        other_user_thread_poll.refresh_from_db()

    with pytest.raises(PollVote.DoesNotExist):
        other_user_thread_poll_vote.refresh_from_db()


def test_merge_threads_deletes_old_threads(
    default_category, sibling_category, thread, user_thread, other_user_thread
):
    synchronize_category(default_category)

    thread.category = default_category
    user_thread.category = default_category
    other_user_thread.category = default_category

    assert default_category.last_thread

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        user_thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        other_user_thread.refresh_from_db()

    assert default_category.last_thread is None
