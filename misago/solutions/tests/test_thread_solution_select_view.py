from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ..solutions import select_thread_solution


def test_thread_solution_select_view_sets_thread_solution(
    thread_reply_factory, user_client, user, other_user, default_category, user_thread
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)

    response = user_client.post(
        reverse(
            "misago:thread-solution-select",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
                "post_id": solution.id,
            },
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
        + f"#post-{solution.id}"
    )

    user_thread.refresh_from_db()
    assert user_thread.solution == solution
    assert user_thread.solution_by == other_user
    assert user_thread.solution_by_name == other_user.username
    assert user_thread.solution_by_slug == other_user.slug
    assert user_thread.solution_selected_at
    assert user_thread.solution_selected_by == user
    assert user_thread.solution_selected_by_name == user.username
    assert user_thread.solution_selected_by_slug == user.slug


def test_thread_solution_select_view_changes_thread_solution(
    thread_reply_factory, user_client, user, other_user, default_category, user_thread
):
    default_category.enable_solutions = True
    default_category.save()

    old_solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, old_solution, user)

    new_solution = thread_reply_factory(user_thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:thread-solution-select",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
                "post_id": new_solution.id,
            },
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
        + f"#post-{new_solution.id}"
    )

    user_thread.refresh_from_db()
    assert user_thread.solution == new_solution
    assert user_thread.solution_by == user
    assert user_thread.solution_by_name == user.username
    assert user_thread.solution_by_slug == user.slug
    assert user_thread.solution_selected_at
    assert user_thread.solution_selected_by == user
    assert user_thread.solution_selected_by_name == user.username
    assert user_thread.solution_selected_by_slug == user.slug


def test_thread_solution_select_view_does_nothing_if_new_solution_is_same_as_current_one(
    thread_reply_factory, user_client, user, other_user, default_category, user_thread
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)

    response = user_client.post(
        reverse(
            "misago:thread-solution-select",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
                "post_id": solution.id,
            },
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
        + f"#post-{solution.id}"
    )

    user_thread.refresh_from_db()
    assert user_thread.solution == solution
    assert user_thread.solution_by == other_user
    assert user_thread.solution_by_name == other_user.username
    assert user_thread.solution_by_slug == other_user.slug
    assert user_thread.solution_selected_at
    assert user_thread.solution_selected_by == user
    assert user_thread.solution_selected_by_name == user.username
    assert user_thread.solution_selected_by_slug == user.slug


def test_thread_solution_select_view_returns_error_if_post_doesn_validate(
    user_client, default_category, user_thread
):
    default_category.enable_solutions = True
    default_category.save()

    response = user_client.post(
        reverse(
            "misago:thread-solution-select",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
                "post_id": user_thread.first_post_id,
            },
        )
    )

    assert_contains(
        response,
        "Original posts can&#x27;t be selected as thread solutions.",
        status_code=403,
    )

    user_thread.refresh_from_db()
    assert user_thread.solution is None
    assert user_thread.solution_by is None
    assert user_thread.solution_by_name is None
    assert user_thread.solution_by_slug is None
    assert user_thread.solution_selected_at is None
    assert user_thread.solution_selected_by is None
    assert user_thread.solution_selected_by_name is None
    assert user_thread.solution_selected_by_slug is None


def test_thread_solution_select_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:thread-solution-select",
            kwargs={"thread_id": 100, "slug": "not-found", "post_id": 1},
        )
    )
    assert response.status_code == 404


def test_thread_solution_select_view_returns_error_404_if_thread_post_doesnt_exist(
    user_client, user_thread
):
    response = user_client.post(
        reverse(
            "misago:thread-solution-select",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
                "post_id": user_thread.last_post_id + 1,
            },
        )
    )
    assert response.status_code == 404


def test_thread_solution_select_view_returns_error_404_if_post_doesnt_exist_in_thread(
    user_client, thread, user_thread
):
    post = thread.first_post

    response = user_client.post(
        reverse(
            "misago:thread-post-like",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert response.status_code == 404
