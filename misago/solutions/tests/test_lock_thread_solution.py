from ..solutions import lock_thread_solution, select_thread_solution


def test_lock_thread_solution_locks_thread_solution_by_user(
    moderator, user, thread, other_user_reply
):
    select_thread_solution(thread, other_user_reply, user)
    lock_thread_solution(thread, moderator)

    assert thread.solution_is_locked
    assert thread.solution_locked_at
    assert thread.solution_locked_by == moderator
    assert thread.solution_locked_by_name == moderator.username
    assert thread.solution_locked_by_slug == moderator.slug

    thread.refresh_from_db()

    assert thread.solution_is_locked
    assert thread.solution_locked_at
    assert thread.solution_locked_by == moderator
    assert thread.solution_locked_by_name == moderator.username
    assert thread.solution_locked_by_slug == moderator.slug


def test_lock_thread_solution_locks_thread_solution_by_deleted_user(
    user, thread, other_user_reply
):
    select_thread_solution(thread, other_user_reply, user)
    lock_thread_solution(thread, "Moderator")

    assert thread.solution_is_locked
    assert thread.solution_locked_at
    assert thread.solution_locked_by is None
    assert thread.solution_locked_by_name == "Moderator"
    assert thread.solution_locked_by_slug is None

    thread.refresh_from_db()

    assert thread.solution_is_locked
    assert thread.solution_locked_at
    assert thread.solution_locked_by is None
    assert thread.solution_locked_by_name == "Moderator"
    assert thread.solution_locked_by_slug is None


def test_lock_thread_solution_doesnt_save_changes_if_commit_is_false(
    django_assert_num_queries, moderator, user, thread, other_user_reply
):
    select_thread_solution(thread, other_user_reply, user)

    with django_assert_num_queries(0):
        lock_thread_solution(thread, moderator, commit=False)

    assert thread.solution_is_locked
    assert thread.solution_locked_at
    assert thread.solution_locked_by == moderator
    assert thread.solution_locked_by_name == moderator.username
    assert thread.solution_locked_by_slug == moderator.slug

    thread.refresh_from_db()

    assert not thread.solution_is_locked
    assert thread.solution_locked_at is None
    assert thread.solution_locked_by is None
    assert thread.solution_locked_by_name is None
    assert thread.solution_locked_by_slug is None
