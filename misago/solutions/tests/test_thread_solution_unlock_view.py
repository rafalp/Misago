from django.urls import reverse

from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ..solutions import select_thread_solution, lock_thread_solution


def test_thread_solution_unlock_view_unlocks_thread_solution(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    other_user,
    default_category,
    user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)
    lock_thread_solution(user_thread, moderator)

    response = moderator_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    user_thread.refresh_from_db()
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None


def test_thread_solution_unlock_view_returns_redirect_to_solution(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    other_user,
    default_category,
    user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)
    lock_thread_solution(user_thread, moderator)

    response = moderator_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"next": "post"},
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
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None


def test_thread_solution_unlock_view_returns_redirect_to_next_url(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    other_user,
    default_category,
    user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)
    lock_thread_solution(user_thread, moderator)

    response = moderator_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {
            "next": reverse(
                "misago:thread",
                kwargs={
                    "thread_id": user_thread.id,
                    "slug": user_thread.slug,
                    "page": 42,
                },
            )
        },
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
            "page": 42,
        },
    )

    user_thread.refresh_from_db()
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None


def test_thread_solution_unlock_view_returns_redirect_to_thread_for_invalid_next_url(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    other_user,
    default_category,
    user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)
    lock_thread_solution(user_thread, moderator)

    response = moderator_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        ),
        {"next": "invalid"},
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    user_thread.refresh_from_db()
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None


def test_thread_solution_unlock_view_does_nothing_if_thread_solution_is_unlocked(
    thread_reply_factory,
    moderator_client,
    moderator,
    user,
    other_user,
    default_category,
    user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)

    response = moderator_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    user_thread.refresh_from_db()
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None


def test_thread_solution_unlock_view_does_nothing_if_thread_has_no_solution(
    moderator_client, default_category, user_thread
):
    default_category.enable_solutions = True
    default_category.save()

    response = moderator_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    user_thread.refresh_from_db()
    assert not user_thread.solution_is_locked
    assert user_thread.solution_locked_at is None
    assert user_thread.solution_locked_by is None
    assert user_thread.solution_locked_by_name is None
    assert user_thread.solution_locked_by_slug is None


def test_thread_solution_unlock_view_returns_error_403_if_user_has_no_unlock_solution_permission(
    thread_reply_factory,
    user_client,
    default_category,
    moderator,
    user,
    other_user,
    user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(user_thread, poster=other_user)
    select_thread_solution(user_thread, solution, user)
    lock_thread_solution(user_thread, moderator)

    response = user_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )

    assert_contains(
        response,
        "You can&#x27;t unlock thread solutions.",
        status_code=403,
    )

    user_thread.refresh_from_db()
    assert user_thread.solution_is_locked
    assert user_thread.solution_locked_at
    assert user_thread.solution_locked_by == moderator
    assert user_thread.solution_locked_by_name == moderator.username
    assert user_thread.solution_locked_by_slug == moderator.slug


def test_thread_solution_unlock_view_returns_error_404_if_thread_doesnt_exist(
    user_client,
):
    response = user_client.post(
        reverse(
            "misago:thread-solution-unlock",
            kwargs={"thread_id": 100, "slug": "not-found"},
        )
    )
    assert response.status_code == 404
