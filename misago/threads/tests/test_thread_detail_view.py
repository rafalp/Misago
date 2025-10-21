from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains, assert_not_contains


def test_thread_detail_view_shows_error_404_if_thread_doesnt_exist(user_client):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
            },
        )
    )
    assert response.status_code == 404


def test_thread_detail_view_shows_error_404_to_users_who_cant_see_thread_category(
    user_client, members_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        category_id=thread.category_id,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_thread_detail_view_shows_error_404_to_users_who_cant_browse_thread_category(
    user_client, members_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        category_id=thread.category_id,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_thread_detail_view_shows_error_403_to_users_who_cant_browse_thread_category_with_delayed_check(
    user_client, members_group, default_category, thread
):
    default_category.delay_browse_check = True
    default_category.save()

    CategoryGroupPermission.objects.filter(
        group=members_group,
        category_id=default_category.id,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(
        response, "You can&#x27;t browse the contents of this category.", 403
    )


def test_thread_detail_view_shows_error_404_to_users_who_cant_see_thread(
    user_client, thread
):
    thread.is_hidden = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_thread_detail_view_shows_user_their_thread(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
    )
    assert_contains(response, user_thread.title)


def test_thread_detail_view_shows_user_other_user_thread(
    user_client, other_user_thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_thread.title)


def test_thread_detail_view_shows_category_moderator_other_user_thread(
    user_client, user, other_user_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[other_user_thread.category_id],
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_thread.title)


def test_thread_detail_view_shows_global_moderator_other_user_thread(
    moderator_client, other_user_thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_thread.title)


def test_thread_detail_view_shows_user_deleted_user_thread(user_client, thread):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_category_moderator_deleted_user_thread(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_global_moderator_deleted_user_thread(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_user_their_thread_in_htmx(user_client, user_thread):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_thread.title)


def test_thread_detail_view_shows_user_other_user_thread_in_htmx(
    user_client, other_user_thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_thread.title)


def test_thread_detail_view_shows_category_moderator_other_user_thread_in_htmx(
    user_client, user, other_user_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[other_user_thread.category_id],
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_thread.title)


def test_thread_detail_view_shows_global_moderator_other_user_thread_in_htmx(
    moderator_client, other_user_thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_thread.title)


def test_thread_detail_view_shows_user_deleted_user_thread_in_htmx(
    user_client, user, thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_category_moderator_deleted_user_thread_in_htmx(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_global_moderator_deleted_user_thread_in_htmx(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_returns_redirect_to_valid_url_if_slug_is_invalid(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": "invalid-slug",
            },
        )
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
        },
    )


def test_thread_detail_view_ignores_invalid_slug_in_htmx(user_client, thread):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": "invalid-slug",
            },
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200


def test_thread_detail_view_shows_error_404_if_private_thread_is_accessed(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_not_contains(response, user_private_thread.title, status_code=404)
