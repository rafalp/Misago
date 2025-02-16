import pytest
from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...categories.models import Category
from ...test import assert_contains, assert_has_error_message
from ...threads.models import Thread
from .categories_tree import assert_valid_categories_tree


def test_category_delete_form_renders(default_category, admin_client):
    response = admin_client.get(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
    )
    assert_contains(response, "Delete category")


def test_category_delete_form_shows_error_if_category_doesnt_exist(
    default_category, admin_client
):
    response = admin_client.get(
        reverse(
            "misago:admin:categories:delete", kwargs={"pk": default_category.pk + 1}
        ),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def test_category_delete_form_shows_error_if_category_is_root(
    root_category, admin_client
):
    response = admin_client.get(
        reverse("misago:admin:categories:delete", kwargs={"pk": root_category.pk}),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def test_only_leaf_category_is_deleted(root_category, default_category, admin_client):
    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": ""},
    )
    assert response.status_code == 302

    assert_valid_categories_tree([(root_category, 0, 1, 2)])


def test_category_with_child_is_deleted_together_with_child(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": ""},
    )
    assert response.status_code == 302

    assert_valid_categories_tree([(root_category, 0, 1, 2)])


def test_category_with_child_is_deleted_and_child_is_made_top_category(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": str(root_category.id), "move_contents_to": ""},
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (child_category, 1, 2, 3),
        ]
    )


def test_category_with_child_is_deleted_and_child_is_moved_to_sibling(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": str(sibling_category.id), "move_contents_to": ""},
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (sibling_category, 1, 2, 5),
            (child_category, 2, 3, 4),
        ]
    )


def test_category_with_child_cant_be_deleted_because_move_children_to_is_invalid(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": str(child_category.id + 1), "move_contents_to": ""},
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 5),
            (child_category, 2, 3, 4),
        ]
    )


def test_category_with_children_cant_be_deleted_because_move_children_to_is_deleted(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    deep_category = Category(name="Child Category", slug="child-category")
    deep_category.insert_at(child_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": str(child_category.id), "move_contents_to": ""},
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 8),
            (default_category, 1, 2, 7),
            (child_category, 2, 3, 6),
            (deep_category, 3, 4, 5),
        ]
    )


def test_category_with_children_cant_be_deleted_because_deep_move_children_to_is_deleted(
    root_category, default_category, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    deep_category = Category(name="Deep Category", slug="deep-category")
    deep_category.insert_at(child_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": str(deep_category.id), "move_contents_to": ""},
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 8),
            (default_category, 1, 2, 7),
            (child_category, 2, 3, 6),
            (deep_category, 3, 4, 5),
        ]
    )


def test_category_is_deleted_and_sibling_edges_are_updated(
    root_category, default_category, admin_client
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": ""},
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (sibling_category, 1, 2, 3),
        ]
    )


def test_category_is_deleted_and_both_siblings_edges_are_updated(
    root_category, default_category, admin_client
):
    first_category = Category(name="F Category", slug="f-category")
    first_category.insert_at(root_category, position="first-child", save=True)

    last_category = Category(name="l Category", slug="l-category")
    last_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": ""},
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (first_category, 1, 2, 3),
            (last_category, 1, 4, 5),
        ]
    )


def test_category_thread_is_deleted_with_category(
    root_category, default_category, thread, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": ""},
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 2),
        ]
    )

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()


def test_category_thread_is_moved_to_other_category_on_delete(
    root_category, default_category, thread, admin_client
):
    sibling_category = Category(name="Child Category", slug="child-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": str(sibling_category.id)},
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (sibling_category, 1, 2, 3),
        ]
    )

    sibling_category.refresh_from_db()
    assert sibling_category.last_thread == thread

    thread.refresh_from_db()
    assert thread.category == sibling_category


def test_category_thread_is_moved_to_kept_child_category_on_delete(
    root_category, default_category, thread, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={
            "move_children_to": str(root_category.id),
            "move_contents_to": str(child_category.id),
        },
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (child_category, 1, 2, 3),
        ]
    )

    child_category.refresh_from_db()
    assert child_category.last_thread == thread

    thread.refresh_from_db()
    assert thread.category == child_category


def test_category_threads_cant_be_moved_to_deleted_child_category(
    root_category, default_category, thread, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": str(child_category.id)},
    )
    assert_contains(
        response,
        "You are trying to move this category&#x27;s contents to a child category that will also be deleted.",
    )

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 5),
            (child_category, 2, 3, 4),
        ]
    )

    thread.refresh_from_db()
    assert thread.category == default_category


def test_category_threads_cant_be_moved_to_deleted_deep_category(
    root_category, default_category, thread, admin_client
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    deep_category = Category(name="Deep Category", slug="deep-category")
    deep_category.insert_at(child_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": str(deep_category.id)},
    )
    assert_contains(
        response,
        "You are trying to move this category&#x27;s contents to a child category that will also be deleted.",
    )

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 8),
            (default_category, 1, 2, 7),
            (child_category, 2, 3, 6),
            (deep_category, 3, 4, 5),
        ]
    )

    thread.refresh_from_db()
    assert thread.category == default_category


def test_category_threads_cant_be_moved_to_root_category(
    root_category, default_category, thread, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": str(root_category.id)},
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )

    thread.refresh_from_db()
    assert thread.category == default_category


def test_category_threads_cant_be_moved_to_nonexisting_category(
    root_category, default_category, thread, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:delete", kwargs={"pk": default_category.pk}),
        data={"move_children_to": "", "move_contents_to": str(default_category.id + 1)},
    )
    assert_contains(response, "That choice is not one of the available choices.")

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )

    thread.refresh_from_db()
    assert thread.category == default_category


def test_deleting_category_invalidates_categories_cache(default_category, admin_client):
    with assert_invalidates_cache(CacheName.CATEGORIES):
        admin_client.post(
            reverse(
                "misago:admin:categories:delete", kwargs={"pk": default_category.pk}
            ),
            data={"move_children_to": "", "move_contents_to": ""},
        )


def test_deleting_category_invalidates_permissions_cache(
    default_category, admin_client
):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        admin_client.post(
            reverse(
                "misago:admin:categories:delete", kwargs={"pk": default_category.pk}
            ),
            data={"move_children_to": "", "move_contents_to": ""},
        )


def test_deleting_category_invalidates_moderators_cache(default_category, admin_client):
    with assert_invalidates_cache(CacheName.MODERATORS):
        admin_client.post(
            reverse(
                "misago:admin:categories:delete", kwargs={"pk": default_category.pk}
            ),
            data={"move_children_to": "", "move_contents_to": ""},
        )
