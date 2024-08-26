from unittest.mock import Mock

import pytest
from django.utils import timezone

from ...permissions.enums import CategoryPermission
from ...permissions.proxy import UserPermissionsProxy
from ...testutils import (
    grant_category_group_permissions,
    remove_category_group_permissions,
)
from ..components import get_categories_data, get_subcategories_data
from ..models import Category


@pytest.fixture
def mock_request(dynamic_settings, user, cache_versions):
    user_permissions = UserPermissionsProxy(user, cache_versions)
    return Mock(
        settings=dynamic_settings,
        user=user,
        user_permissions=user_permissions,
    )


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
    assert not category_data["children_unread"]


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
    assert not data[0]["children_unread"]

    assert data[1]["category"] == sibling_category
    assert data[1]["threads"] == sibling_category.threads
    assert data[1]["posts"] == sibling_category.posts
    assert data[1]["children_threads"] == sibling_category.threads
    assert data[1]["children_posts"] == sibling_category.posts
    assert data[1]["children"] == []
    assert not data[1]["children_unread"]


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
    assert not category_data["children_unread"]


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
    assert not category_data["children_unread"]
    assert len(category_data["children"]) == 1

    child_data = category_data["children"][0]
    assert child_data["category"] == child_category
    assert child_data["threads"] == child_category.threads
    assert child_data["posts"] == child_category.posts
    assert child_data["children_threads"] == child_category.threads
    assert child_data["children_posts"] == child_category.posts
    assert child_data["children"] == []
    assert not child_data["children_unread"]


def test_categories_component_data_includes_unread_category(
    default_category, mock_request, user
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    default_category.last_post_on = timezone.now()
    default_category.save()

    data = get_categories_data(mock_request)
    assert len(data) == 1

    category_data = data[0]
    assert category_data["category"] == default_category
    assert category_data["threads"] == default_category.threads
    assert category_data["posts"] == default_category.posts
    assert category_data["children_threads"] == default_category.threads
    assert category_data["children_posts"] == default_category.posts
    assert category_data["children"] == []
    assert category_data["children_unread"]


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
    assert not child_data["children_unread"]


def test_get_subcategories_data_includes_unread_child_category(
    user, default_category, mock_request
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    default_category.threads = 12
    default_category.posts = 15
    default_category.save()

    child_category = Category(
        name="Child Category",
        slug="child-category",
        threads=42,
        posts=100,
        last_post_on=timezone.now(),
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
    assert child_data["children_unread"]
