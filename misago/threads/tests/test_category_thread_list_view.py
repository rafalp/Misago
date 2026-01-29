from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse

from ...categories.enums import CategoryChildrenComponent
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains, assert_not_contains


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


def test_category_thread_list_view_returns_error_404_for_private_threads_category(
    client, private_threads_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": private_threads_category.id,
                "slug": private_threads_category.slug,
            },
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_for_category_with_invalid_tree_id(
    client, default_category
):
    Category.objects.filter(id=default_category.id).update(tree_id=9001)

    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_redirect_to_valid_url_if_slug_is_invalid(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": "invalid",
            },
        )
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:category-thread-list",
        kwargs={
            "category_id": default_category.id,
            "slug": default_category.slug,
        },
    )


def test_category_thread_list_view_returns_error_404_for_top_level_vanilla_category_without_children(
    default_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_for_top_level_vanilla_category_with_invisible_children(
    default_category, child_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    CategoryGroupPermission.objects.filter(category=child_category).delete()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 404


def test_category_thread_list_view_renders_for_top_level_vanilla_category_with_children(
    default_category, child_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 200


def test_category_thread_list_view_renders_for_nested_vanilla_category_without_children(
    child_category, client
):
    child_category.is_vanilla = True
    child_category.list_children_threads = False
    child_category.save()

    response = client.get(child_category.get_absolute_url())
    assert response.status_code == 200


def test_category_thread_list_view_renders_full_subcategories_component(
    client, guests_group, default_category
):
    default_category.children_categories_component = CategoryChildrenComponent.FULL
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "list-group-category")


def test_category_thread_list_view_renders_dropdown_subcategories_component(
    client, guests_group, default_category
):
    default_category.children_categories_component = CategoryChildrenComponent.DROPDOWN
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "dropdown-category")


def test_category_thread_list_view_renders_empty_to_anonymous_users(
    client, default_category
):
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


def test_category_thread_list_view_renders_empty_to_category_moderators(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

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


def test_category_thread_list_view_renders_empty_to_anonymous_users_in_htmx(
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


def test_category_thread_list_view_renders_empty_to_category_moderators_in_htmx(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

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


def test_category_thread_list_view_for_child_category_renders_empty_to_anonymous_users(
    client, child_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        )
    )
    assert_contains(response, child_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_for_child_category_renders_empty_to_users(
    user_client, child_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        )
    )
    assert_contains(response, child_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_for_child_category_renders_empty_to_category_moderators(
    user_client, user, child_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[child_category.id],
    )

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        )
    )
    assert_contains(response, child_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_for_child_category_renders_empty_to_global_moderators(
    moderator_client, child_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        )
    )
    assert_contains(response, child_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_for_child_category_renders_empty_to_anonymous_users_in_htmx(
    client, child_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_for_child_category_renders_empty_to_users_in_htmx(
    user_client, child_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_for_child_category_renders_empty_to_category_moderators_in_htmx(
    user_client, user, child_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[child_category.id],
    )

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_for_child_category_renders_empty_to_global_moderators_in_htmx(
    moderator_client, child_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": child_category.id, "slug": child_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_displays_deleted_user_thread_to_anonymous_user(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_deleted_user_thread_to_user(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_deleted_user_thread_to_category_moderator(
    thread_factory, user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_deleted_user_thread_to_global_moderator(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_user_thread_to_anonymous_user(
    thread_factory, client, user, default_category
):
    thread = thread_factory(default_category, starter=user)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_user_thread_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_user_thread_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_user_thread_to_global_moderator(
    thread_factory, moderator_client, user, default_category
):
    thread = thread_factory(default_category, starter=user)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_user_own_thread_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_doesnt_display_user_unapproved_thread_to_anonymous_user(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_unapproved=True)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_doesnt_display_user_unapproved_thread_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_unapproved=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_displays_user_unapproved_thread_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, starter=other_user, is_unapproved=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_displays_user_unapproved_thread_to_global_moderator(
    thread_factory, moderator_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_unapproved=True)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_displays_user_own_unapproved_thread_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_unapproved=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_doesnt_display_user_hidden_thread_to_anonymous_user(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_hidden=True)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-hidden")


def test_category_thread_list_view_doesnt_display_user_hidden_thread_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_hidden=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-hidden")


def test_category_thread_list_view_displays_user_hidden_thread_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, starter=other_user, is_hidden=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-hidden")


def test_category_thread_list_view_displays_user_hidden_thread_to_global_moderator(
    thread_factory, moderator_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_hidden=True)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-hidden")


def test_category_thread_list_view_doesnt_display_user_own_hidden_thread_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_hidden=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-hidden")


def test_category_thread_list_view_displays_thread_without_flags(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")


def test_category_thread_list_view_displays_globally_pinned_thread(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=2)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-globally")


def test_category_thread_list_view_displays_globally_pinned_thread_from_other_category(
    thread_factory, client, guests_group, other_user, default_category, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    )

    thread = thread_factory(sibling_category, starter=other_user, weight=2)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-globally")


def test_category_thread_list_view_displays_locally_pinned_thread(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=1)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally")


def test_category_thread_list_view_doesnt_display_thread_pinned_in_child_category_flag_to_anonymous_user(
    thread_factory, client, other_user, default_category, child_category
):
    thread = thread_factory(child_category, starter=other_user, weight=1)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_thread_list_view_doesnt_display_thread_pinned_in_child_category_flag_to_user(
    thread_factory, user_client, other_user, default_category, child_category
):
    thread = thread_factory(child_category, starter=other_user, weight=1)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_thread_list_view_displays_thread_pinned_in_child_category_flag_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category, child_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[child_category.id],
    )

    thread = thread_factory(child_category, starter=other_user, weight=1)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_thread_list_view_displays_thread_pinned_in_child_category_flag_to_global_moderator(
    thread_factory, moderator_client, other_user, default_category, child_category
):
    thread = thread_factory(child_category, starter=other_user, weight=1)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


def test_category_thread_list_view_displays_thread_with_poll(
    thread_factory, poll_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)
    poll_factory(thread)

    response = client.get(default_category.get_absolute_url())

    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-poll")


def test_category_thread_list_view_displays_solved_thread(
    thread_factory, thread_reply_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)
    thread.best_answer = thread_reply_factory(thread)
    thread.save()

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-answered")


def test_category_thread_list_view_displays_closed_thread(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_closed=True)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-closed")


def test_category_thread_list_view_doesnt_display_thread_unapproved_posts_flag_to_anonymous_user(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_doesnt_display_thread_unapproved_posts_flag_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_displays_thread_unapproved_posts_flag_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_displays_thread_unapproved_posts_flag_to_global_moderator(
    thread_factory, moderator_client, other_user, default_category
):
    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_doesnt_display_own_thread_unapproved_posts_flag_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, has_unapproved_posts=True)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


def test_category_thread_list_view_doesnt_display_deleted_user_thread_to_anonymous_user_if_show_started_only_is_enabled(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)


def test_category_thread_list_view_doesnt_display_deleted_user_thread_to_user_if_show_started_only_is_enabled(
    thread_factory, user_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)


def test_category_thread_list_view_displays_deleted_user_thread_to_category_moderator_if_show_started_only_is_enabled(
    thread_factory, user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_deleted_user_thread_to_global_moderator_if_show_started_only_is_enabled(
    thread_factory, moderator_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_doesnt_display_user_thread_to_anonymous_user_if_show_started_only_is_enabled(
    thread_factory, client, other_user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)


def test_category_thread_list_view_doesnt_display_user_thread_to_user_if_show_started_only_is_enabled(
    thread_factory, user_client, other_user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_not_contains(response, thread.title)


def test_category_thread_list_view_displays_user_thread_to_category_moderator_if_show_started_only_is_enabled(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_user_thread_to_global_moderator_if_show_started_only_is_enabled(
    thread_factory, moderator_client, other_user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_user_own_thread_to_user_if_show_started_only_is_enabled(
    thread_factory, user_client, user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_globally_pinned_thread_to_anonymous_user_if_show_started_only_is_enabled(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=2)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_globally_pinned_thread_to_user_if_show_started_only_is_enabled(
    thread_factory, user_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=2)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_category_pinned_thread_to_anonymous_user_if_show_started_only_is_enabled(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=1)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_category_pinned_thread_to_user_if_show_started_only_is_enabled(
    thread_factory, user_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=1)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_thread_with_user_starter_and_deleted_last_poster(
    thread_factory, thread_reply_factory, client, user, default_category
):
    thread = thread_factory(default_category, starter=user)
    thread_reply_factory(thread)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


def test_category_thread_list_view_displays_thread_with_deleted_starter_and_user_last_poster(
    thread_factory, thread_reply_factory, client, user, default_category
):
    thread = thread_factory(default_category)
    thread_reply_factory(thread, poster=user)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


def test_category_thread_list_view_displays_thread_with_different_deleted_starter_and_last_poster(
    thread_factory, thread_reply_factory, client, default_category
):
    thread = thread_factory(default_category, starter="SomeStarter")
    thread_reply_factory(thread, poster="OtherPoster")

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


def test_category_thread_list_view_displays_thread_with_different_starter_and_last_poster(
    thread_factory, thread_reply_factory, client, user, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)
    thread_reply_factory(thread, poster=user)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


@override_dynamic_settings(
    threads_list_item_categories_component="breadcrumbs",
)
def test_category_thread_list_view_displays_category_thread_using_breadcrumbs_component(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


@override_dynamic_settings(
    threads_list_item_categories_component="labels",
)
def test_category_thread_list_view_displays_category_thread_using_labels_component(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


@override_dynamic_settings(
    threads_list_item_categories_component="breadcrumbs",
)
def test_category_thread_list_view_displays_child_category_thread_using_breadcrumbs_component(
    thread_factory, client, default_category, child_category
):
    thread = thread_factory(child_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


@override_dynamic_settings(
    threads_list_item_categories_component="labels",
)
def test_category_thread_list_view_displays_child_category_thread_using_labels_component(
    thread_factory, client, default_category, child_category
):
    thread = thread_factory(child_category)

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


def test_category_thread_list_view_includes_child_category_thread(
    thread_factory, user_client, user, other_user, default_category
):
    default_category.list_children_threads = True
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    thread = thread_factory(child_category, starter=other_user)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.BROWSE,
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, thread.title)


def test_category_thread_list_view_excludes_child_category_thread_if_list_children_threads_is_false(
    thread_factory, user_client, user, other_user, default_category
):
    default_category.list_children_threads = False
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    thread = thread_factory(child_category, starter=other_user)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.BROWSE,
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")
    assert_not_contains(response, thread.title)


def test_category_thread_list_view_displays_thread_in_htmx(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(
        default_category.get_absolute_url(),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)


def test_category_thread_list_view_displays_thread_with_animation_in_htmx(
    thread_factory, user_client, default_category
):
    category_url = default_category.get_absolute_url()
    thread = thread_factory(default_category)

    response = user_client.get(
        category_url + "?animate_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-animate")


def test_category_thread_list_view_displays_thread_without_animation_in_htmx(
    thread_factory, user_client, default_category
):
    category_url = default_category.get_absolute_url()
    thread = thread_factory(default_category)

    response = user_client.get(
        category_url + f"?animate_new={thread.last_post_id + 1}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


def test_category_thread_list_view_disables_animations_without_htmx(
    thread_factory, user_client, default_category
):
    category_url = default_category.get_absolute_url()
    thread = thread_factory(default_category)

    response = user_client.get(
        category_url + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


def test_category_thread_list_view_raises_404_error_if_filter_is_invalid(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
                "filter": "invalid",
            },
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_filters_threads(
    thread_factory, user_client, user, default_category
):
    visible_thread = thread_factory(default_category, starter=user)
    hidden_thread = thread_factory(default_category)

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
                "filter": "my",
            },
        )
    )
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
def test_category_thread_list_view_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client, default_category
):
    category_url = default_category.get_absolute_url()

    response = user_client.get(category_url)

    assert response.status_code == 302
    assert response["location"] == category_url + "?cursor=10"

    mock_pagination.assert_called_once()


def test_category_thread_list_view_renders_unread_thread(
    thread_factory, user, user_client, default_category
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)


def test_category_thread_list_view_marks_unread_category_without_unread_threads_as_read(
    thread_factory, user_client, user, default_category
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    threads = (
        thread_factory(
            default_category,
            started_at=-900,
        ),
        thread_factory(
            default_category,
            started_at=-600,
        ),
    )

    for thread in threads:
        ReadThread.objects.create(
            user=user,
            category=default_category,
            thread=thread,
            read_time=thread.last_posted_at,
        )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    ReadCategory.objects.get(user=user, category=default_category)


def test_category_thread_list_view_marks_unread_category_with_read_entry_without_unread_threads_as_read(
    thread_factory, user_client, user, default_category
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    thread = thread_factory(
        default_category,
        started_at=-2400,
    )

    read_category = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=thread.last_posted_at,
    )

    read_thread = thread_factory(
        default_category,
        started_at=-1200,
    )

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=read_thread,
        read_time=read_thread.last_posted_at,
    )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    new_read_category = ReadCategory.objects.get(user=user, category=default_category)
    assert new_read_category.id == read_category.id
    assert new_read_category.read_time > read_category.read_time


def test_category_thread_list_view_doesnt_mark_unread_category_with_unread_thread_as_read(
    thread_factory, user_client, user, default_category
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    read_thread = thread_factory(
        default_category,
        started_at=-900,
    )

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=read_thread,
        read_time=read_thread.last_posted_at,
    )

    thread_factory(
        default_category,
        started_at=-600,
    )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert ReadThread.objects.exists()
    assert not ReadCategory.objects.exists()
