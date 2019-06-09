from unittest.mock import Mock

import pytest

from ..models import Category
from ..utils import get_categories_tree, get_category_path


@pytest.fixture
def categories_tree(root_category, default_category):
    Category(name="Category A", slug="category-a").insert_at(
        root_category, position="last-child", save=True
    )
    Category(name="Category E", slug="category-e").insert_at(
        root_category, position="last-child", save=True
    )

    category_a = Category.objects.get(slug="category-a")

    Category(name="Category B", slug="category-b").insert_at(
        category_a, position="last-child", save=True
    )

    category_b = Category.objects.get(slug="category-b")

    category_c = Category(name="Subcategory C", slug="subcategory-c").insert_at(
        category_b, position="last-child", save=True
    )
    category_d = Category(name="Subcategory D", slug="subcategory-d").insert_at(
        category_b, position="last-child", save=True
    )

    category_e = Category.objects.get(slug="category-e")
    Category(name="Subcategory F", slug="subcategory-f").insert_at(
        category_e, position="last-child", save=True
    )

    return {
        "root": root_category,
        "first": default_category,
        "a": Category.objects.get(slug="category-a"),
        "b": Category.objects.get(slug="category-b"),
        "c": Category.objects.get(slug="subcategory-c"),
        "d": Category.objects.get(slug="subcategory-d"),
        "e": Category.objects.get(slug="category-e"),
        "f": Category.objects.get(slug="subcategory-f"),
    }


@pytest.fixture
def full_access_user_acl(categories_tree, user_acl):
    user_acl = user_acl.copy()
    categories_acl = {"categories": {}, "visible_categories": []}
    for category in Category.objects.all_categories():
        categories_acl["visible_categories"].append(category.id)
        categories_acl["categories"][category.id] = {"can_see": 1, "can_browse": 1}
    user_acl.update(categories_acl)
    return user_acl


@pytest.fixture
def request_mock(user, full_access_user_acl, dynamic_settings):
    return Mock(settings=dynamic_settings, user=user, user_acl=full_access_user_acl)


def test_tree_getter_defaults_to_returning_top_level_categories(
    request_mock, categories_tree
):
    assert get_categories_tree(request_mock) == [
        categories_tree["first"],
        categories_tree["a"],
        categories_tree["e"],
    ]


def test_tree_getter_returns_category_subtree(request_mock, categories_tree):
    assert get_categories_tree(request_mock, categories_tree["a"]) == [
        categories_tree["b"]
    ]


def test_tree_getter_returns_empty_list_for_leaf_category(
    request_mock, categories_tree
):
    assert get_categories_tree(request_mock, categories_tree["f"]) == []


def test_path_getter_returns_path_to_category(request_mock, categories_tree):
    for node in get_categories_tree(request_mock):
        parent_nodes = len(get_category_path(node))
        assert parent_nodes == node.level
