from django.urls import reverse

from ...permissions.models import Moderator
from ...test import assert_contains, assert_not_contains
from ..models import PrivateThreadMember


def test_private_thread_detail_view_displays_login_required_page_to_anonymous_user(
    db, client
):
    response = client.get(
        reverse(
            "misago:private-thread", kwargs={"thread_id": 1, "slug": "private-thread"}
        )
    )
    assert_contains(response, "Sign in to view private threads", status_code=401)


def test_private_thread_detail_view_shows_error_403_to_users_without_private_threads_permission(
    user_client, members_group, other_user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_detail_view_shows_error_404_if_thread_doesnt_exist(user_client):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_detail_view_shows_error_404_to_users_who_cant_see_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_detail_view_shows_user_their_thread(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, user_private_thread.title)


def test_private_thread_detail_view_shows_user_other_user_thread(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_detail_view_shows_private_threads_moderator_other_user_thread(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_detail_view_shows_global_moderator_other_user_thread(
    moderator_client, other_user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_detail_view_shows_user_deleted_user_thread(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert_contains(response, private_thread.title)


def test_private_thread_detail_view_shows_private_threads_moderator_deleted_user_thread(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert_contains(response, private_thread.title)


def test_private_thread_detail_view_shows_global_moderator_deleted_user_thread(
    moderator_client, moderator, private_thread
):
    PrivateThreadMember.objects.create(user=moderator, thread=private_thread)

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert_contains(response, private_thread.title)


def test_private_thread_detail_view_shows_user_their_thread_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)


def test_private_thread_detail_view_shows_user_other_user_thread_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_detail_view_shows_private_threads_moderator_other_user_thread_in_htmx(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_detail_view_shows_global_moderator_other_user_thread_in_htmx(
    moderator_client, other_user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_detail_view_shows_user_deleted_user_thread_in_htmx(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, private_thread.title)


def test_private_thread_detail_view_shows_private_threads_moderator_deleted_user_thread_in_htmx(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, private_thread.title)


def test_private_thread_detail_view_shows_global_moderator_deleted_user_thread_in_htmx(
    moderator_client, moderator, private_thread
):
    PrivateThreadMember.objects.create(user=moderator, thread=private_thread)

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, private_thread.title)


def test_private_thread_detail_view_returns_redirect_to_valid_url_if_slug_is_invalid(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": "invalid-slug",
            },
        )
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )


def test_private_thread_detail_view_ignores_invalid_slug_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": "invalid-slug",
            },
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200


def test_private_thread_detail_view_shows_thread_members_to_thread_owner(
    user_client, user_private_thread, user, other_user, moderator
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "3 members")
    assert_contains(response, user.username)
    assert_contains(response, other_user.username)
    assert_contains(response, moderator.username)


def test_private_thread_detail_view_shows_thread_members_to_other_user(
    user_client, other_user_private_thread, user, other_user, moderator
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "3 members")
    assert_contains(response, user.username)
    assert_contains(response, other_user.username)
    assert_contains(response, moderator.username)


def test_private_thread_detail_view_shows_thread_members_to_moderator(
    moderator_client, user_private_thread, user, other_user, moderator
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, "3 members")
    assert_contains(response, user.username)
    assert_contains(response, other_user.username)
    assert_contains(response, moderator.username)


def test_private_thread_detail_view_shows_error_404_if_thread_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert_not_contains(response, thread.title, status_code=404)
