from ...categories.models import Category
from ...categories.proxy import CategoriesProxy
from ...permissions.enums import CategoryPermission
from ...testutils import (
    grant_category_group_permissions,
    remove_category_group_permissions,
)
from ..categories import get_categories_menu_data, serialize_menu_item


def serialize_last_menu_item(category: Category) -> dict:
    data = serialize_menu_item(category)
    data["last"] = True
    return data


def test_get_categories_menu_data_returns_empty_categories_menu(
    user_permissions_factory, default_category, user, cache_versions
):
    remove_category_group_permissions(default_category, user.group)

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert get_categories_menu_data(categories) == []


def test_get_categories_menu_data_returns_categories_menu_with_one_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert get_categories_menu_data(categories) == [
        serialize_menu_item(default_category),
    ]


def test_get_categories_menu_data_returns_categories_menu_with_two_categories(
    user_permissions_factory, root_category, default_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert get_categories_menu_data(categories) == [
        serialize_last_menu_item(default_category),
        serialize_menu_item(sibling_category),
    ]


def test_get_categories_menu_data_returns_categories_menu_with_vanilla_category(
    user_permissions_factory, root_category, default_category, user, cache_versions
):
    sibling_category = Category(
        name="Sibling Category", slug="sibling-category", is_vanilla=True
    )
    sibling_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(sibling_category, position="last-child", save=True)

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert get_categories_menu_data(categories) == [
        serialize_last_menu_item(default_category),
        serialize_menu_item(sibling_category),
        serialize_menu_item(child_category),
    ]


def test_get_categories_menu_data_returns_categories_menu_without_empty_vanilla_category(
    user_permissions_factory, root_category, default_category, user, cache_versions
):
    sibling_category = Category(
        name="Sibling Category", slug="sibling-category", is_vanilla=True
    )
    sibling_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(sibling_category, position="last-child", save=True)

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert get_categories_menu_data(categories) == [
        serialize_menu_item(default_category),
    ]


def test_get_categories_menu_data_sets_last_flag_on_categories_menu_vanilla_category_last_item(
    user_permissions_factory, root_category, default_category, user, cache_versions
):
    sibling_category = Category(
        name="Sibling Category", slug="sibling-category", is_vanilla=True
    )
    sibling_category.insert_at(root_category, position="first-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(sibling_category, position="last-child", save=True)

    default_category.refresh_from_db()

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert get_categories_menu_data(categories) == [
        serialize_menu_item(sibling_category),
        serialize_last_menu_item(child_category),
        serialize_menu_item(default_category),
    ]
