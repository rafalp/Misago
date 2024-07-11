from unittest.mock import Mock

import pytest

from ...permissions.enums import CategoryPermission
from ...permissions.proxy import UserPermissionsProxy
from ...testutils import (
    grant_category_group_permissions,
    remove_category_group_permissions,
)
from ..components import (
    get_categories_component,
    get_categories_data,
    get_subcategories_data,
)
from ..models import Category


@pytest.fixture
def mock_request(user, cache_versions):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    return Mock(user=user, user_permissions=user_permissions)


def test_categories_component_returns_template_name(mock_request):
    data = get_categories_component(mock_request)
    assert data["template_name"]


def test_categories_component_returns_category_data(default_category, mock_request):
    data = get_categories_component(mock_request)
    assert len(data["categories"]) == 1
    assert data["categories"] == get_categories_data(mock_request)


def test_categories_component_data_returns_empty_categories_list(
    default_category, mock_request
):
    remove_category_group_permissions(default_category, mock_request.user.group)

    data = get_categories_data(mock_request)
    assert len(data) == 0


def test_categories_component_data_includes_category(default_category, mock_request):
    data = get_categories_data(mock_request)
    assert len(data) == 1

    category_data = data[0]
    assert category_data["category"] == default_category
    assert category_data["threads"] == default_category.threads
    assert category_data["posts"] == default_category.posts
    assert category_data["children_threads"] == default_category.threads
    assert category_data["children_posts"] == default_category.posts
    assert category_data["children"] == []


def test_categories_component_data_excludes_invisible_category(
    root_category, default_category, mock_request
):
    sibling_category = Category(name="Sibling Category", slug="sibling-category")
    sibling_category.insert_at(root_category, position="last-child", save=True)

    data = get_categories_data(mock_request)
    assert len(data) == 1

    category_data = data[0]
    assert category_data["category"] == default_category
    assert category_data["children"] == []


def test_categories_component_data_includes_visible_category(
    root_category, default_category, mock_request
):
    sibling_category = Category(
        name="Sibling Category", slug="sibling-category", threads=42, posts=100
    )
    sibling_category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(
        sibling_category,
        mock_request.user.group,
        CategoryPermission.SEE,
    )

    data = get_categories_data(mock_request)
    assert len(data) == 2

    assert data[0]["category"] == default_category
    assert data[0]["threads"] == default_category.threads
    assert data[0]["posts"] == default_category.posts
    assert data[0]["children_threads"] == default_category.threads
    assert data[0]["children_posts"] == default_category.posts
    assert data[0]["children"] == []

    assert data[1]["category"] == sibling_category
    assert data[1]["threads"] == sibling_category.threads
    assert data[1]["posts"] == sibling_category.posts
    assert data[1]["children_threads"] == sibling_category.threads
    assert data[1]["children_posts"] == sibling_category.posts
    assert data[1]["children"] == []


def test_categories_component_data_excludes_invisible_child_category(
    root_category, default_category, mock_request
):
    child_category = Category(
        name="Child Category", slug="child-category", threads=42, posts=100
    )
    child_category.insert_at(root_category, position="last-child", save=True)

    data = get_categories_data(mock_request)
    assert len(data) == 1

    category_data = data[0]
    assert category_data["category"] == default_category
    assert category_data["category"] == default_category
    assert category_data["threads"] == default_category.threads
    assert category_data["posts"] == default_category.posts
    assert category_data["children_threads"] == default_category.threads
    assert category_data["children_posts"] == default_category.posts
    assert category_data["children"] == []


def test_categories_component_data_includes_visible_child_category(
    default_category, mock_request
):
    default_category.threads = 12
    default_category.posts = 15
    default_category.save()

    child_category = Category(
        name="Child Category", slug="child-category", threads=42, posts=100
    )
    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        mock_request.user.group,
        CategoryPermission.SEE,
    )

    data = get_categories_data(mock_request)
    assert len(data) == 1

    category_data = data[0]
    assert category_data["category"] == default_category
    assert category_data["category"] == default_category
    assert category_data["threads"] == default_category.threads
    assert category_data["posts"] == default_category.posts
    assert (
        category_data["children_threads"]
        == default_category.threads + child_category.threads
    )
    assert (
        category_data["children_posts"] == default_category.posts + child_category.posts
    )
    assert len(category_data["children"]) == 1

    child_data = category_data["children"][0]
    assert child_data["category"] == child_category
    assert child_data["threads"] == child_category.threads
    assert child_data["posts"] == child_category.posts
    assert child_data["children_threads"] == child_category.threads
    assert child_data["children_posts"] == child_category.posts
    assert child_data["children"] == []


def test_get_subcategories_data_returns_empty_categories_list(
    default_category, mock_request
):
    data = get_subcategories_data(mock_request, default_category)
    assert len(data) == 0


def test_get_subcategories_data_excludes_sibling_categories(
    root_category, default_category, mock_request
):
    sibling_category = Category(
        name="Sibling Category", slug="sibling-category", threads=42, posts=100
    )
    sibling_category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(
        sibling_category,
        mock_request.user.group,
        CategoryPermission.SEE,
    )

    data = get_subcategories_data(mock_request, default_category)
    assert len(data) == 0


def test_get_subcategories_data_excludes_invisible_child_category(
    default_category, mock_request
):
    child_category = Category(
        name="Child Category", slug="child-category", threads=42, posts=100
    )
    child_category.insert_at(default_category, position="last-child", save=True)

    data = get_subcategories_data(mock_request, default_category)
    assert len(data) == 0


def test_get_subcategories_data_includes_visible_child_category(
    default_category, mock_request
):
    default_category.threads = 12
    default_category.posts = 15
    default_category.save()

    child_category = Category(
        name="Child Category", slug="child-category", threads=42, posts=100
    )
    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        mock_request.user.group,
        CategoryPermission.SEE,
    )

    data = get_subcategories_data(mock_request, default_category)
    assert len(data) == 1

    child_data = data[0]
    assert child_data["category"] == child_category
    assert child_data["threads"] == child_category.threads
    assert child_data["posts"] == child_category.posts
    assert child_data["children_threads"] == child_category.threads
    assert child_data["children_posts"] == child_category.posts
    assert child_data["children"] == []
