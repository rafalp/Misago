from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains


def test_category_thread_list_view_returns_error_404_if_category_doesnt_exist(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id * 100,
                "slug": default_category.slug,
            },
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_if_guest_cant_see_it(
    client, sibling_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_if_user_cant_see_it(
    user_client, sibling_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_if_global_moderator_cant_see_it(
    moderator_client, sibling_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_403_if_guest_cant_browse_it(
    client, guests_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )

    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_category_thread_list_view_returns_error_403_if_user_cant_browse_it(
    user_client, members_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_category_thread_list_view_returns_error_403_if_global_moderator_cant_browse_it(
    moderator_client, moderators_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )

    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_category_thread_list_view_renders_if_guest_cant_browse_it_but_check_is_delayed(
    client, guests_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )

    sibling_category.delay_browse_check = True
    sibling_category.save()

    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(response, sibling_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_if_user_cant_browse_it_but_check_is_delayed(
    user_client, members_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )

    sibling_category.delay_browse_check = True
    sibling_category.save()

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(response, sibling_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_if_global_moderator_cant_browse_it_but_check_is_delayed(
    moderator_client, moderators_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )

    sibling_category.delay_browse_check = True
    sibling_category.save()

    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(response, sibling_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_guests(client, default_category):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_users(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_global_moderators(
    moderator_client, default_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_guests_in_htmx(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_users_in_htmx(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_global_moderators_in_htmx(
    moderator_client, default_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")
