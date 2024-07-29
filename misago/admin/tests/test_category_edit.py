from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...categories.models import Category
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_has_error_message
from .categories_tree import assert_valid_categories_tree

category_new = reverse("misago:admin:categories:new")


def test_edit_category_form_renders(admin_client, default_category):
    response = admin_client.get(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk})
    )
    assert_contains(response, "Edit category")
    assert_contains(response, default_category.name)


def test_edit_category_form_shows_error_if_category_doesnt_exist(
    default_category, admin_client
):
    response = admin_client.get(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk + 1}),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def test_edit_category_form_shows_error_if_category_is_root(
    root_category, admin_client
):
    response = admin_client.get(
        reverse("misago:admin:categories:edit", kwargs={"pk": root_category.pk}),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def form_data(category: Category, new_data: dict | None = None) -> dict:
    data = {
        "new_parent": str(category.parent_id),
        "name": category.name or "",
        "short_name": category.short_name or "",
        "color": category.color or "",
        "description": category.description or "",
        "css_class": category.css_class or "",
        "copy_permissions": "",
        "allow_polls": category.allow_polls,
        "delay_browse_check": category.delay_browse_check,
        "show_started_only": category.show_started_only,
        "is_closed": category.is_closed,
        "is_vanilla": category.is_vanilla,
        "list_children_threads": category.list_children_threads,
        "children_categories_component": category.children_categories_component,
        "require_threads_approval": category.require_threads_approval,
        "require_replies_approval": category.require_replies_approval,
        "require_edits_approval": category.require_edits_approval,
        "prune_started_after": str(category.prune_started_after),
        "prune_replied_after": str(category.prune_replied_after),
        "archive_pruned_in": str(category.archive_pruned_in or ""),
    }

    if new_data:
        data.update(new_data)

    return data


def test_edit_category_form_moves_category_under_other_category(
    root_category, default_category, admin_client
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
        form_data(default_category, {"new_parent": str(sibling_category.id)}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (sibling_category, 1, 2, 5),
            (default_category, 2, 3, 4),
        ]
    )


def test_edit_category_form_moves_child_category_to_top_level(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": child_category.pk}),
        form_data(child_category, {"new_parent": str(root_category.id)}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (child_category, 1, 4, 5),
        ]
    )


def test_edit_category_form_invalidates_categories_cache(
    default_category, admin_client
):
    with assert_invalidates_cache(CacheName.CATEGORIES):
        response = admin_client.post(
            reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
            form_data(default_category),
        )
        assert response.status_code == 302


def test_edit_category_form_invalidates_moderators_cache(
    default_category, admin_client
):
    with assert_invalidates_cache(CacheName.MODERATORS):
        response = admin_client.post(
            reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
            form_data(default_category),
        )
        assert response.status_code == 302


def test_edit_category_form_invalidates_permissions_cache(
    default_category, admin_client
):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        response = admin_client.post(
            reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
            form_data(default_category),
        )
        assert response.status_code == 302


def test_edit_category_form_shows_error_if_category_is_moved_to_self(
    root_category, default_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
        form_data(default_category, {"new_parent": str(default_category.id)}),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_edit_category_form_shows_error_if_category_is_moved_to_own_child_category(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
        form_data(default_category, {"new_parent": str(child_category.id)}),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 5),
            (child_category, 2, 3, 4),
        ]
    )


def test_edit_category_form_shows_error_if_category_is_moved_to_invalid_category(
    root_category, default_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
        form_data(default_category, {"new_parent": str(default_category.id + 1)}),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_edit_category_form_changes_top_category_to_vanilla(
    root_category, default_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
        form_data(default_category, {"is_vanilla": True}),
    )
    assert response.status_code == 302

    default_category.refresh_from_db()
    assert default_category.is_vanilla

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_edit_category_form_shows_error_if_child_category_is_changed_to_vanilla(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": child_category.pk}),
        form_data(child_category, {"is_vanilla": True}),
    )
    assert_contains(response, "Only top-level categories can be set as vanilla.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 5),
            (child_category, 2, 3, 4),
        ]
    )


def test_edit_category_form_fails_if_vanilla_category_without_threads_and_categories_dropdown(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        reverse("misago:admin:categories:edit", kwargs={"pk": default_category.pk}),
        form_data(
            default_category,
            {
                "new_parent": str(root_category.id),
                "is_vanilla": True,
                "list_children_threads": False,
                "children_categories_component": "dropdown",
            },
        ),
    )
    assert_contains(
        response,
        "This choice is not available for vanilla categories with disabled listing",
    )

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )
