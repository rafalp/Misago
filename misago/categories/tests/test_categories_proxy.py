from ...categories.models import Category
from ...permissions.enums import CategoryPermission
from ...permissions.proxy import UserPermissionsProxy
from ...testutils import (
    grant_category_group_permissions,
    remove_category_group_permissions,
)
from ..categories import get_category_data
from ..proxy import CategoriesProxy


def get_category_data_dict(category: Category):
    return get_category_data(category.__dict__)


def test_categories_proxy_loads_categories_visible_to_anonymous_user(
    default_category, anonymous_user, cache_versions
):
    user_permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.categories[default_category.id] == get_category_data_dict(
        default_category
    )


def test_categories_proxy_loads_categories_visible_to_user(
    default_category, user, cache_versions
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.categories[default_category.id] == get_category_data_dict(
        default_category
    )


def test_categories_proxy_excludes_categories_inaccessible_by_user(
    root_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert sibling_category.id not in categories.categories


def test_categories_proxy_list_has_categories_visible_to_user(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.categories_list == [
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_returns_category_parents_with_self(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

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

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_category_parents(child_category.id) == [
        get_category_data_dict(child_category),
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_returns_category_parents_without_self(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

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

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_category_parents(child_category.id, include_self=False) == [
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_returns_category_path_with_self(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

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

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_category_path(child_category.id) == [
        get_category_data_dict(default_category),
        get_category_data_dict(child_category),
    ]


def test_categories_proxy_returns_category_path_without_self(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

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

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_category_path(child_category.id, include_self=False) == [
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_returns_category_descendants(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(
        name="Sibling Category", slug="sibling-category", is_vanilla=True
    )
    sibling_category.insert_at(root_category, position="first-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    deep_category = Category(name="Deep Category", slug="deep-category")
    deep_category.insert_at(child_category, position="last-child", save=True)

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

    grant_category_group_permissions(
        deep_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_category_descendants(default_category.id) == [
        get_category_data_dict(default_category),
        get_category_data_dict(child_category),
        get_category_data_dict(deep_category),
    ]


def test_categories_proxy_returns_category_descendants_without_self(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(
        name="Sibling Category", slug="sibling-category", is_vanilla=True
    )
    sibling_category.insert_at(root_category, position="first-child", save=True)

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    deep_category = Category(name="Deep Category", slug="deep-category")
    deep_category.insert_at(child_category, position="last-child", save=True)

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

    grant_category_group_permissions(
        deep_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_category_descendants(
        default_category.id, include_self=False
    ) == [
        get_category_data_dict(child_category),
        get_category_data_dict(deep_category),
    ]


def test_categories_proxy_returns_empty_categories_menu(
    default_category, user, cache_versions
):
    remove_category_group_permissions(default_category, user.group)

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_categories_menu() == []


def test_categories_proxy_returns_categories_menu_with_one_category(
    default_category, user, cache_versions
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_categories_menu() == [
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_returns_categories_menu_with_two_categories(
    root_category, default_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_categories_menu() == [
        get_category_data_dict(default_category),
        get_category_data_dict(sibling_category),
    ]


def test_categories_proxy_returns_categories_menu_with_vanilla_category(
    root_category, default_category, user, cache_versions
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

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_categories_menu() == [
        get_category_data_dict(default_category),
        get_category_data_dict(sibling_category),
        get_category_data_dict(child_category),
    ]


def test_categories_proxy_returns_categories_menu_without_empty_vanilla_category(
    root_category, default_category, user, cache_versions
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

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_categories_menu() == [
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_sets_last_flag_on_categories_menu_vanilla_category_last_item(
    root_category, default_category, user, cache_versions
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

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_categories_menu() == [
        get_category_data_dict(sibling_category),
        dict(**get_category_data_dict(child_category), last=True),
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_returns_default_category_thread_path(
    default_category, user, cache_versions
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_thread_categories(default_category.id) == [
        get_category_data_dict(default_category),
    ]


def test_categories_proxy_returns_default_category_thread_path_from_default_category(
    default_category, user, cache_versions
):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert (
        categories.get_thread_categories(default_category.id, default_category.id) == []
    )


def test_categories_proxy_returns_child_category_thread_path(
    default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    default_category.refresh_from_db()

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_thread_categories(child_category.id) == [
        get_category_data_dict(default_category),
        get_category_data_dict(child_category),
    ]


def test_categories_proxy_returns_child_category_thread_path_from_default_category(
    default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    default_category.refresh_from_db()

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_thread_categories(child_category.id, default_category.id) == [
        get_category_data_dict(child_category),
    ]


def test_categories_proxy_returns_child_category_thread_path_from_child_category(
    default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    default_category.refresh_from_db()

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_thread_categories(child_category.id, child_category.id) == []


def test_categories_proxy_returns_sibling_category_thread_path_from_child_category(
    root_category, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    default_category.refresh_from_db()

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )
    grant_category_group_permissions(
        sibling_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(user_permissions, cache_versions)

    assert categories.get_thread_categories(sibling_category.id, child_category.id) == [
        get_category_data_dict(sibling_category),
    ]
