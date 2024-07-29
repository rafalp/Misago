from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...categories.models import Category
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from .categories_tree import assert_valid_categories_tree

category_new = reverse("misago:admin:categories:new")


def test_new_category_form_renders(admin_client):
    response = admin_client.get(category_new)
    assert_contains(response, "New category")


def form_data(new_data: dict) -> dict:
    data = {
        "name": "New Category",
        "short_name": "",
        "color": "",
        "description": "",
        "css_class": "",
        "copy_permissions": "",
        "allow_polls": True,
        "delay_browse_check": False,
        "show_started_only": False,
        "is_closed": False,
        "is_vanilla": False,
        "list_children_threads": True,
        "children_categories_component": "full",
        "require_threads_approval": False,
        "require_replies_approval": False,
        "require_edits_approval": False,
        "prune_started_after": "0",
        "prune_replied_after": "0",
        "archive_pruned_in": "",
    }
    data.update(new_data)
    return data


def test_new_category_form_creates_new_top_category(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(root_category.id),
            }
        ),
    )
    assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (new_category, 1, 4, 5),
        ]
    )


def test_new_category_form_creates_new_child_category(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(default_category.id),
            }
        ),
    )
    assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 5),
            (new_category, 2, 3, 4),
        ]
    )


def test_new_category_form_copies_category_permissions(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(root_category.id),
                "copy_permissions": str(default_category.id),
            }
        ),
    )
    assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (new_category, 1, 4, 5),
        ]
    )

    assert CategoryGroupPermission.objects.filter(category=new_category).exists()


def test_new_category_form_creates_category_with_archive(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(root_category.id),
                "archive_pruned_in": str(default_category.id),
            }
        ),
    )
    assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert new_category.archive_pruned_in == default_category

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (new_category, 1, 4, 5),
        ]
    )


def test_new_category_form_invalidates_categories_cache(
    admin_client, root_category, default_category
):
    with assert_invalidates_cache(CacheName.CATEGORIES):
        response = admin_client.post(
            category_new,
            form_data(
                {
                    "new_parent": str(root_category.id),
                }
            ),
        )
        assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (new_category, 1, 4, 5),
        ]
    )


def test_new_category_form_invalidates_moderators_cache(
    admin_client, root_category, default_category
):
    with assert_invalidates_cache(CacheName.MODERATORS):
        response = admin_client.post(
            category_new,
            form_data(
                {
                    "new_parent": str(root_category.id),
                }
            ),
        )
        assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (new_category, 1, 4, 5),
        ]
    )


def test_new_category_form_invalidates_permissions_cache(
    admin_client, root_category, default_category
):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        response = admin_client.post(
            category_new,
            form_data(
                {
                    "new_parent": str(root_category.id),
                }
            ),
        )
        assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (new_category, 1, 4, 5),
        ]
    )


def test_new_category_form_fails_if_parent_doesnt_exist(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(default_category.id + 1),
            }
        ),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_new_category_form_creates_vanilla_category(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data({"new_parent": str(root_category.id), "is_vanilla": True}),
    )
    assert response.status_code == 302

    new_category = Category.objects.get(slug="new-category")
    assert new_category.is_vanilla

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (new_category, 1, 4, 5),
        ]
    )


def test_new_category_form_fails_if_vanilla_category_with_parent(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data({"new_parent": str(default_category.id), "is_vanilla": True}),
    )
    assert_contains(response, "Only top-level categories can be set as vanilla.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_new_category_form_fails_if_vanilla_category_without_threads_and_categories_dropdown(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(root_category.id),
                "is_vanilla": True,
                "list_children_threads": False,
                "children_categories_component": "dropdown",
            }
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


def test_new_category_form_fails_if_copy_permissions_doesnt_exist(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(default_category.id),
                "copy_permissions": str(default_category.id + 1),
            }
        ),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_new_category_form_fails_if_copy_permissions_is_root(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(default_category.id),
                "copy_permissions": str(root_category.id),
            }
        ),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_new_category_form_fails_if_archive_doesnt_exist(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(default_category.id),
                "archive_pruned_in": str(default_category.id + 1),
            }
        ),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_new_category_form_fails_if_archive_is_root(
    admin_client, root_category, default_category
):
    response = admin_client.post(
        category_new,
        form_data(
            {
                "new_parent": str(default_category.id),
                "archive_pruned_in": str(root_category.id),
            }
        ),
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )
