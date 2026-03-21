from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ..solutions import select_thread_solution


def test_thread_solution_clear_view_clears_thread_solution(
    thread_reply_factory, user_client, user, other_user, default_category, user_thread
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)

    response = user_client.post(
        reverse(
            "misago:thread-solution-clear",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert user_thread.solution is None
    assert user_thread.solution_by is None
    assert user_thread.solution_by_name is None
    assert user_thread.solution_by_slug is None
    assert user_thread.solution_selected_at is None
    assert user_thread.solution_selected_by is None
    assert user_thread.solution_selected_by_name is None
    assert user_thread.solution_selected_by_slug is None


def test_thread_solution_clear_view_does_nothing_if_thread_has_no_solution(
    user_client, default_category, user_thread
):
    default_category.enable_solutions = True
    default_category.save()

    response = user_client.post(
        reverse(
            "misago:thread-solution-clear",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert response.status_code == 302

    user_thread.refresh_from_db()
    assert user_thread.solution is None
    assert user_thread.solution_by is None
    assert user_thread.solution_by_name is None
    assert user_thread.solution_by_slug is None
    assert user_thread.solution_selected_at is None
    assert user_thread.solution_selected_by is None
    assert user_thread.solution_selected_by_name is None
    assert user_thread.solution_selected_by_slug is None


def test_thread_solution_clear_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:thread-solution-clear",
            kwargs={"thread_id": 100, "slug": "not-found"},
        )
    )
    assert response.status_code == 404
