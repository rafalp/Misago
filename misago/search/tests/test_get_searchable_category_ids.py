from ...categories.models import Category
from ...categories.proxy import CategoriesProxy
from ...permissions.enums import CategoryPermission
from ...testutils import grant_category_group_permissions
from ..categories import get_searchable_category_ids


def test_get_searchable_category_ids_returns_browseable_categories(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    searchable_categories = get_searchable_category_ids(user_permissions, categories)
    assert searchable_categories == {default_category.id}


def test_get_searchable_category_ids_includes_child_categories(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    searchable_categories = get_searchable_category_ids(user_permissions, categories)
    assert searchable_categories == {default_category.id, child_category.id}


def test_get_searchable_category_ids_excludes_visible_non_browseable_categories(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    searchable_categories = get_searchable_category_ids(user_permissions, categories)
    assert searchable_categories == {default_category.id}


def test_get_searchable_category_ids_excludes_visible_and_browseable_vanilla_categories(
    user_permissions_factory, root_category, default_category, user, cache_versions
):
    other_category = Category(
        name="Other Category",
        slug="other-category",
        is_vanilla=True,
    )
    other_category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(
        other_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    searchable_categories = get_searchable_category_ids(user_permissions, categories)
    assert searchable_categories == {default_category.id}
