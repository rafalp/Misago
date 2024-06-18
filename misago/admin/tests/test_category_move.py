from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...categories.models import Category
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_has_error_message
from .categories_tree import assert_valid_categories_tree


def test_category_move_up_shows_error_if_category_doesnt_exist(
    default_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:up", kwargs={"pk": default_category.pk + 1}),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def test_category_move_down_shows_error_if_category_doesnt_exist(
    default_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:down", kwargs={"pk": default_category.pk + 1}),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def test_category_move_up_shows_error_if_category_is_root(root_category, admin_client):
    response = admin_client.post(
        reverse("misago:admin:categories:up", kwargs={"pk": root_category.pk}),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def test_category_move_down_shows_error_if_category_is_root(
    root_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:down", kwargs={"pk": root_category.pk}),
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested category does not exist.")


def test_only_category_move_up_does_nothing(
    root_category, default_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:up", kwargs={"pk": default_category.pk}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_only_category_move_down_does_nothing(
    root_category, default_category, admin_client
):
    response = admin_client.post(
        reverse("misago:admin:categories:down", kwargs={"pk": default_category.pk}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 4),
            (default_category, 1, 2, 3),
        ]
    )


def test_top_category_move_up_updates_tree(
    root_category, default_category, admin_client
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:up", kwargs={"pk": sibling_category.pk}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (sibling_category, 1, 2, 3),
            (default_category, 1, 4, 5),
        ]
    )


def test_top_category_move_down_updates_tree(
    root_category, default_category, admin_client
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="first-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:down", kwargs={"pk": sibling_category.pk}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (sibling_category, 1, 4, 5),
        ]
    )


def test_middle_category_move_up_updates_tree(
    root_category, default_category, admin_client
):
    middle_category = Category(name="Middle Category", slug="middle-category")
    middle_category.insert_at(root_category, position="last-child", save=True)

    bottom_category = Category(name="Bottom Category", slug="bottom-category")
    bottom_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:up", kwargs={"pk": middle_category.pk}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 8),
            (middle_category, 1, 2, 3),
            (default_category, 1, 4, 5),
            (bottom_category, 1, 6, 7),
        ]
    )


def test_middle_category_move_down_updates_tree(
    root_category, default_category, admin_client
):
    middle_category = Category(name="Middle Category", slug="middle-category")
    middle_category.insert_at(root_category, position="last-child", save=True)

    bottom_category = Category(name="Bottom Category", slug="bottom-category")
    bottom_category.insert_at(root_category, position="last-child", save=True)

    response = admin_client.post(
        reverse("misago:admin:categories:down", kwargs={"pk": middle_category.pk}),
    )
    assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 8),
            (default_category, 1, 2, 3),
            (bottom_category, 1, 4, 5),
            (middle_category, 1, 6, 7),
        ]
    )


def test_ategory_move_up_invalidates_categories_cache(
    root_category, default_category, admin_client
):
    other_category = Category(name="Other Category", slug="other-category")
    other_category.insert_at(root_category, position="first-child", save=True)

    with assert_invalidates_cache(CacheName.CATEGORIES):
        response = admin_client.post(
            reverse("misago:admin:categories:up", kwargs={"pk": default_category.pk}),
        )
        assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (default_category, 1, 2, 3),
            (other_category, 1, 4, 5),
        ]
    )


def test_category_move_down_invalidates_categories_cache(
    root_category, default_category, admin_client
):
    other_category = Category(name="Other Category", slug="other-category")
    other_category.insert_at(root_category, position="last-child", save=True)

    with assert_invalidates_cache(CacheName.CATEGORIES):
        response = admin_client.post(
            reverse("misago:admin:categories:down", kwargs={"pk": default_category.pk}),
        )
        assert response.status_code == 302

    assert_valid_categories_tree(
        [
            (root_category, 0, 1, 6),
            (other_category, 1, 2, 3),
            (default_category, 1, 4, 5),
        ]
    )
