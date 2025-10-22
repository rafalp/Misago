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


def test_thread_detail_view_shows_anonymous_user_deleted_user_thread(client, thread):
    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_anonymous_user_user_thread(client, user_thread):
    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
    )
    assert_contains(response, user_thread.title)


def test_thread_detail_view_shows_anonymous_user_category_moderator_thread(
    client, user, user_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[user_thread.category_id],
    )

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
    )
    assert_contains(response, user_thread.title)


def test_thread_detail_view_shows_anonymous_user_global_moderator_thread(
    client, user, user_thread
):
    Moderator.objects.create(user=user)

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
    )
    assert_contains(response, user_thread.title)


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


def test_thread_detail_view_shows_user_category_moderator_thread(
    user_client, other_user, other_user_thread
):
    Moderator.objects.create(
        user=other_user,
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


def test_thread_detail_view_shows_user_global_moderator_thread(
    user_client, other_user, other_user_thread
):
    Moderator.objects.create(user=other_user)

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


def test_thread_detail_view_shows_anonymous_user_deleted_user_thread_in_htmx(
    client, thread
):
    response = client.get(
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


def test_thread_detail_view_shows_anonymous_user_user_thread_in_htmx(
    client, user_thread
):
    response = client.get(
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


def test_thread_detail_view_shows_anonymous_user_category_moderator_thread_in_htmx(
    client, user, user_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[user_thread.category_id],
    )

    response = client.get(
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


def test_thread_detail_view_shows_anonymous_user_global_moderator_thread_in_htmx(
    client, user, user_thread
):
    Moderator.objects.create(user=user)

    response = client.get(
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


def test_thread_detail_view_shows_user_category_moderator_thread_in_htmx(
    user_client, other_user, other_user_thread
):
    Moderator.objects.create(
        user=other_user,
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


def test_thread_detail_view_shows_user_global_moderator_thread_in_htmx(
    user_client, other_user, other_user_thread
):
    Moderator.objects.create(user=other_user)

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


def test_thread_detail_view_shows_error_404_to_anonymous_user_for_deleted_user_thread_in_show_started_only(
    client, default_category, thread
):
    default_category.show_started_only = True
    default_category.save()

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_thread_detail_view_shows_error_404_to_anonymous_user_for_user_thread_in_show_started_only(
    client, default_category, other_user_thread
):
    default_category.show_started_only = True
    default_category.save()

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_thread_detail_view_shows_deleted_user_category_pinned_thread_to_anonymous_user_in_show_started_only(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=1)

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_deleted_user_globally_pinned_thread_to_anonymous_user_in_show_started_only(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=2)

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, thread.title)


def test_thread_detail_view_shows_error_404_to_user_for_deleted_user_thread_in_show_started_only(
    user_client, default_category, thread
):
    default_category.show_started_only = True
    default_category.save()

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


def test_thread_detail_view_shows_error_404_to_user_for_other_user_thread_in_show_started_only(
    user_client, default_category, other_user_thread
):
    default_category.show_started_only = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_thread_detail_view_shows_user_own_thread_in_show_started_only(
    user_client, default_category, user_thread
):
    default_category.show_started_only = True
    default_category.save()

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


def test_thread_detail_view_shows_deleted_user_category_pinned_thread_to_user_in_show_started_only(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category, weight=1)

    default_category.show_started_only = True
    default_category.set_last_thread(thread)
    default_category.save()

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


def test_thread_detail_view_shows_deleted_user_globally_pinned_thread_to_user_in_show_started_only(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category, weight=2)

    default_category.show_started_only = True
    default_category.set_last_thread(thread)
    default_category.save()

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


def test_thread_detail_view_shows_other_user_category_pinned_thread_to_user_in_show_started_only(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=1)

    default_category.show_started_only = True
    default_category.set_last_thread(thread)
    default_category.save()

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


def test_thread_detail_view_shows_other_user_globally_pinned_thread_to_user_in_show_started_only(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=2)

    default_category.show_started_only = True
    default_category.set_last_thread(thread)
    default_category.save()

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


def test_thread_detail_view_shows_category_moderator_deleted_user_thread_in_show_started_only(
    user_client, user, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    default_category.show_started_only = True
    default_category.save()

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


def test_thread_detail_view_shows_global_moderator_deleted_user_thread_in_show_started_only(
    moderator_client, default_category, thread
):
    default_category.show_started_only = True
    default_category.save()

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


def test_thread_detail_view_shows_category_moderator_other_user_thread_in_show_started_only(
    user_client, user, default_category, other_user_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[other_user_thread.category_id],
    )

    default_category.show_started_only = True
    default_category.save()

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


def test_thread_detail_view_shows_global_moderator_other_user_thread_in_show_started_only(
    moderator_client, default_category, other_user_thread
):
    default_category.show_started_only = True
    default_category.save()

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
