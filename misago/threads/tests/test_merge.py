from ...solutions.solutions import select_thread_solution
from ..merge import get_thread_merge_conflicts


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
