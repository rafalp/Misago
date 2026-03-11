from ..solutions import select_thread_solution


def test_select_thread_solution_sets_thread_solution_by_user(
    user, other_user, thread, other_user_reply
):
    select_thread_solution(thread, other_user_reply, user)

    assert thread.solution == other_user_reply
    assert thread.solution_by == other_user
    assert thread.solution_by_name == other_user.username
    assert thread.solution_by_slug == other_user.slug
    assert thread.solution_selected_at
    assert thread.solution_selected_by == user
    assert thread.solution_selected_by_name == user.username
    assert thread.solution_selected_by_slug == user.slug

    thread.refresh_from_db()

    assert thread.solution == other_user_reply
    assert thread.solution_by == other_user
    assert thread.solution_by_name == other_user.username
    assert thread.solution_by_slug == other_user.slug
    assert thread.solution_selected_at
    assert thread.solution_selected_by == user
    assert thread.solution_selected_by_name == user.username
    assert thread.solution_selected_by_slug == user.slug


def test_select_thread_solution_sets_thread_solution_by_deleted_user(
    other_user, thread, other_user_reply
):
    select_thread_solution(thread, other_user_reply, "DeletedUser")

    assert thread.solution == other_user_reply
    assert thread.solution_by == other_user
    assert thread.solution_by_name == other_user.username
    assert thread.solution_by_slug == other_user.slug
    assert thread.solution_selected_at
    assert thread.solution_selected_by is None
    assert thread.solution_selected_by_name == "DeletedUser"
    assert thread.solution_selected_by_slug is None

    thread.refresh_from_db()

    assert thread.solution == other_user_reply
    assert thread.solution_by == other_user
    assert thread.solution_by_name == other_user.username
    assert thread.solution_by_slug == other_user.slug
    assert thread.solution_selected_at
    assert thread.solution_selected_by is None
    assert thread.solution_selected_by_name == "DeletedUser"
    assert thread.solution_selected_by_slug is None


def test_select_thread_solution_sets_deleted_user_thread_solution_by_user(
    user, thread, reply
):
    select_thread_solution(thread, reply, user)

    assert thread.solution == reply
    assert thread.solution_by is None
    assert thread.solution_by_name == reply.poster_name
    assert thread.solution_by_slug is None
    assert thread.solution_selected_at
    assert thread.solution_selected_by == user
    assert thread.solution_selected_by_name == user.username
    assert thread.solution_selected_by_slug == user.slug

    thread.refresh_from_db()

    assert thread.solution == reply
    assert thread.solution_by is None
    assert thread.solution_by_name == reply.poster_name
    assert thread.solution_by_slug is None
    assert thread.solution_selected_at
    assert thread.solution_selected_by == user
    assert thread.solution_selected_by_name == user.username
    assert thread.solution_selected_by_slug == user.slug


def test_select_thread_solution_doesnt_save_changes_if_commit_is_false(
    django_assert_num_queries, user, other_user, thread, other_user_reply
):
    with django_assert_num_queries(0):
        select_thread_solution(thread, other_user_reply, user, commit=False)

    assert thread.solution == other_user_reply
    assert thread.solution_by == other_user
    assert thread.solution_by_name == other_user.username
    assert thread.solution_by_slug == other_user.slug
    assert thread.solution_selected_at
    assert thread.solution_selected_by == user
    assert thread.solution_selected_by_name == user.username
    assert thread.solution_selected_by_slug == user.slug

    thread.refresh_from_db()

    assert thread.solution is None
    assert thread.solution_by is None
    assert thread.solution_by_name is None
    assert thread.solution_by_slug is None
    assert thread.solution_selected_at is None
    assert thread.solution_selected_by is None
    assert thread.solution_selected_by_name is None
    assert thread.solution_selected_by_slug is None
