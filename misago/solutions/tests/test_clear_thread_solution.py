from ..solutions import clear_thread_solution, select_thread_solution


def test_clear_thread_solution_clears_thread_solution(user, thread, other_user_reply):
    select_thread_solution(thread, other_user_reply, user)

    clear_thread_solution(thread)

    assert thread.solution is None
    assert thread.solution_posted_at is None
    assert thread.solution_by is None
    assert thread.solution_by_name is None
    assert thread.solution_by_slug is None
    assert thread.solution_selected_at is None
    assert thread.solution_selected_by is None
    assert thread.solution_selected_by_name is None
    assert thread.solution_selected_by_slug is None

    thread.refresh_from_db()

    assert thread.solution is None
    assert thread.solution_posted_at is None
    assert thread.solution_by is None
    assert thread.solution_by_name is None
    assert thread.solution_by_slug is None
    assert thread.solution_selected_at is None
    assert thread.solution_selected_by is None
    assert thread.solution_selected_by_name is None
    assert thread.solution_selected_by_slug is None


def test_clear_thread_solution_doesnt_save_changes_if_commit_is_false(
    django_assert_num_queries, user, other_user, thread, other_user_reply
):
    select_thread_solution(thread, other_user_reply, user)

    with django_assert_num_queries(0):
        clear_thread_solution(thread, commit=False)

    assert thread.solution is None
    assert thread.solution_posted_at is None
    assert thread.solution_by is None
    assert thread.solution_by_name is None
    assert thread.solution_by_slug is None
    assert thread.solution_selected_at is None
    assert thread.solution_selected_by is None
    assert thread.solution_selected_by_name is None
    assert thread.solution_selected_by_slug is None

    thread.refresh_from_db()

    assert thread.solution == other_user_reply
    assert thread.solution_posted_at == other_user_reply.posted_at
    assert thread.solution_by == other_user
    assert thread.solution_by_name == other_user.username
    assert thread.solution_by_slug == other_user.slug
    assert thread.solution_selected_at
    assert thread.solution_selected_by == user
    assert thread.solution_selected_by_name == user.username
    assert thread.solution_selected_by_slug == user.slug
