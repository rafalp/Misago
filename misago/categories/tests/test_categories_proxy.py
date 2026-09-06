import pytest

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...testutils import grant_category_group_permissions
from ..categoriesdata import serialize_category_data
from ..models import Category
from ..proxy import CategoriesProxy, CategoryProxy


def get_category_proxy(category: Category) -> CategoryProxy:
    return CategoryProxy(**serialize_category_data(category.__dict__))


def test_categories_proxy_loads_categories_visible_to_anonymous_user(
    user_permissions_factory, default_category, anonymous_user, cache_versions
):
    user_permissions = user_permissions_factory(anonymous_user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert default_category in proxy


def test_categories_proxy_loads_categories_visible_to_user(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert default_category in proxy


def test_categories_proxy_excludes_categories_inaccessible_by_user(
    user_permissions_factory, root_category, user, cache_versions
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert sibling_category not in proxy


def test_categories_proxy_evaluates_to_true_if_it_contains_categories(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)
    assert proxy


def test_categories_proxy_evaluates_to_false_if_it_contains_no_categories(
    user_permissions_factory, default_category, user, cache_versions
):
    CategoryGroupPermission.objects.all().delete()

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)
    assert not proxy


def test_categories_proxy_contains_returns_true_for_contained_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert default_category in proxy
    assert default_category.id in proxy


def test_categories_proxy_contains_returns_false_for_non_contained_category(
    user_permissions_factory, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert sibling_category not in proxy
    assert sibling_category.id not in proxy


def test_categories_proxy_getitem_returns_category_proxy_object_by_id(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy[default_category.id] == get_category_proxy(default_category)


def test_categories_proxy_getitem_raises_key_error_for_nonexisting_id(
    user_permissions_factory, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    with pytest.raises(KeyError):
        proxy[sibling_category.id]


def test_categories_proxy_iter_returns_visible_categories_ids_iterator(
    user_permissions_factory, default_category, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert list(proxy) == [default_category.id]


def test_categories_proxy_len_returns_visible_categories_number(
    user_permissions_factory, default_category, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert len(proxy) == 1


def test_categories_proxy_keys_returns_visible_categories_ids_view(
    user_permissions_factory, default_category, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert list(proxy.keys()) == [default_category.id]


def test_categories_proxy_values_returns_visible_category_proxies_view(
    user_permissions_factory, default_category, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert list(proxy.values()) == [get_category_proxy(default_category)]


def test_categories_proxy_items_returns_visible_categories_id_and_proxy_view(
    user_permissions_factory, default_category, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert list(proxy.items()) == [
        (default_category.id, get_category_proxy(default_category))
    ]


def test_categories_proxy_get_returns_visible_category_proxy(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get(default_category.id) == get_category_proxy(default_category)


def test_categories_proxy_get_returns_false_for_category_without_permission(
    user_permissions_factory, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get(sibling_category.id) is None


def test_categories_proxy_get_parent_returns_categorys_parent(
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
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_parent(child_category) == get_category_proxy(default_category)


def test_categories_proxy_get_parent_returns_none_for_top_level_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_parent(default_category) is None


def test_categories_proxy_get_parent_returns_none_for_parent_category_without_permission(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    default_category.parent_id = default_category.id * 100
    assert proxy.get_parent(default_category) is None


def test_categories_proxy_get_children_returns_direct_children(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    descendant_category = Category(name="Child Category", slug="child-category")
    descendant_category.insert_at(child_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        descendant_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_children(default_category) == [
        get_category_proxy(child_category),
    ]


def test_categories_proxy_get_children_with_self_includes_category(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    descendant_category = Category(name="Child Category", slug="child-category")
    descendant_category.insert_at(child_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        descendant_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_children(default_category, include_self=True) == [
        get_category_proxy(default_category),
        get_category_proxy(child_category),
    ]


def test_categories_proxy_get_children_excludes_children_without_permission(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_children(default_category) == []


def test_categories_proxy_get_children_with_include_self_excludes_parent_without_permission(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_children(child_category, include_self=True) == []


def test_categories_proxy_get_children_returns_empty_list_for_leaf_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_children(default_category) == []


def test_categories_proxy_get_children_with_include_self_returns_leaf_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_children(default_category, include_self=True) == [
        get_category_proxy(default_category),
    ]


def test_categories_proxy_get_ancestors_returns_category_ancestors(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    descendant_category = Category(name="Child Category", slug="child-category")
    descendant_category.insert_at(child_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        descendant_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_ancestors(descendant_category) == [
        get_category_proxy(default_category),
        get_category_proxy(child_category),
    ]


def test_categories_proxy_get_ancestors_with_include_self_returns_category(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    descendant_category = Category(name="Child Category", slug="child-category")
    descendant_category.insert_at(child_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        descendant_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_ancestors(descendant_category, include_self=True) == [
        get_category_proxy(default_category),
        get_category_proxy(child_category),
        get_category_proxy(descendant_category),
    ]


def test_categories_proxy_get_ancestors_returns_empty_list_for_top_level_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_ancestors(default_category) == []


def test_categories_proxy_get_ancestors_with_include_self_returns_top_level_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_ancestors(default_category, include_self=True) == [
        get_category_proxy(default_category),
    ]


def test_categories_proxy_get_descendants_returns_category_descendants(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    descendant_category = Category(name="Child Category", slug="child-category")
    descendant_category.insert_at(child_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        descendant_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_descendants(default_category) == [
        get_category_proxy(child_category),
        get_category_proxy(descendant_category),
    ]


def test_categories_proxy_get_descendants_returns_empty_list_for_leaf_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_descendants(default_category) == []


def test_categories_proxy_get_descendants_with_include_self_returns_leaf_category(
    user_permissions_factory, default_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_descendants(default_category, include_self=True) == [
        get_category_proxy(default_category),
    ]


def test_categories_proxy_get_descendants_with_include_self_returns_category(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    descendant_category = Category(name="Child Category", slug="child-category")
    descendant_category.insert_at(child_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    grant_category_group_permissions(
        descendant_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_descendants(default_category, include_self=True) == [
        get_category_proxy(default_category),
        get_category_proxy(child_category),
        get_category_proxy(descendant_category),
    ]


def test_categories_proxy_get_descendants_excludes_categories_without_permission(
    user_permissions_factory, default_category, user, cache_versions
):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    descendant_category = Category(name="Child Category", slug="child-category")
    descendant_category.insert_at(child_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        user.group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )

    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert proxy.get_descendants(default_category) == [
        get_category_proxy(child_category),
    ]


def test_categories_proxy_can_be_cast_to_dict_with_visible_categories(
    user_permissions_factory, default_category, sibling_category, user, cache_versions
):
    user_permissions = user_permissions_factory(user)
    proxy = CategoriesProxy(user_permissions, cache_versions)

    assert dict(proxy) == {default_category.id: get_category_proxy(default_category)}


def test_category_proxy_is_top_level_attribute_is_true_for_top_level_category(
    default_category,
):
    proxy = get_category_proxy(default_category)
    assert proxy.is_top_level


def test_category_proxy_is_top_level_attribute_is_false_for_child_category(
    child_category,
):
    proxy = get_category_proxy(child_category)
    assert not proxy.is_top_level


def test_category_proxy_is_leaf_attribute_is_true_for_leaf_category(default_category):
    proxy = get_category_proxy(default_category)
    assert proxy.is_leaf


def test_category_proxy_is_leaf_attribute_is_false_for_category_with_children(
    sibling_category,
):
    proxy = get_category_proxy(sibling_category)
    assert not proxy.is_leaf


def test_category_proxy_has_children_attribute_is_false_for_leaf_category(
    default_category,
):
    proxy = get_category_proxy(default_category)
    assert not proxy.has_children


def test_category_proxy_has_children_attribute_is_true_for_category_with_children(
    sibling_category,
):
    proxy = get_category_proxy(sibling_category)
    assert proxy.has_children


def test_category_proxy_is_parent_method_returns_true_if_category_is_parent_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(sibling_category)
    assert proxy.is_parent(child_category)


def test_category_proxy_is_parent_method_returns_false_if_category_is_not_parent_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(child_category)
    assert not proxy.is_parent(sibling_category)


def test_category_proxy_is_child_method_returns_true_if_category_is_child_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(child_category)
    assert proxy.is_child(sibling_category)


def test_category_proxy_is_child_method_returns_false_if_category_is_not_child_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(sibling_category)
    assert not proxy.is_child(child_category)


def test_category_proxy_is_ancestor_method_returns_true_if_category_is_ancestor_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(sibling_category)
    assert proxy.is_ancestor(child_category)


def test_category_proxy_is_ancestor_method_returns_false_if_category_is_not_ancestor_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(child_category)
    assert not proxy.is_ancestor(sibling_category)


def test_category_proxy_is_descendant_method_returns_true_if_category_is_descendant_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(child_category)
    assert proxy.is_descendant(sibling_category)


def test_category_proxy_is_descendant_method_returns_false_if_category_is_not_descendant_of_other_category(
    sibling_category, child_category
):
    proxy = get_category_proxy(sibling_category)
    assert not proxy.is_descendant(child_category)
