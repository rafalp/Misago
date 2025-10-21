from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission


def test_thread_post_solution_view_returns_redirect_to_solution(
    thread_reply_factory, client, user, thread
):
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)
    thread_reply_factory(thread)

    thread.set_best_answer(user, reply)
    thread.save()

    response = client.get(
        reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_post_solution_view_returns_redirect_to_last_post_if_thread_is_not_solved(
    thread_reply_factory, client, thread
):
    thread_reply_factory(thread)
    thread_reply_factory(thread)
    reply = thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
        + f"#post-{reply.id}"
    )


def test_thread_post_solution_view_returns_error_404_if_thread_doesnt_exist(db, client):
    response = client.get(
        reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": 1, "slug": "invalid"},
        )
    )

    assert response.status_code == 404


def test_thread_post_solution_view_returns_error_404_if_user_cant_see_thread(
    thread_reply_factory, client, thread
):
    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 404


def test_thread_post_solution_view_returns_error_403_if_user_cant_see_thread_contents(
    thread_reply_factory, client, thread
):
    thread.category.delay_browse_check = True
    thread.category.save()

    CategoryGroupPermission.objects.filter(
        category=thread.category,
        permission=CategoryPermission.BROWSE,
    ).delete()

    thread_reply_factory(thread)

    response = client.get(
        reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        )
    )

    assert response.status_code == 403


def test_thread_post_solution_view_returns_error_404_if_thread_is_private(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-post-solution",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert response.status_code == 404
