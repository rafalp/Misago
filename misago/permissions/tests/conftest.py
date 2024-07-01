import pytest

from ...categories.models import Category
from ...threads.test import post_thread
from ..enums import CategoryPermission
from ..models import CategoryGroupPermission


@pytest.fixture
def category(root_category):
    category = Category(name="Parent", slug="parent")
    category.insert_at(root_category, position="last-child", save=True)
    return category


@pytest.fixture
def child_category(category):
    category = Category(name="Parent Child", slug="parent-child")
    category.insert_at(category, position="last-child", save=True)
    return category


@pytest.fixture
def sibling_category(root_category):
    category = Category(name="Sibling", slug="sibling")
    category.insert_at(root_category, position="last-child", save=True)
    return category


@pytest.fixture
def category_members_see_permission(category, members_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def category_members_browse_permission(category, members_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def child_category_members_see_permission(child_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def child_category_members_browse_permission(child_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def sibling_category_members_see_permission(sibling_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def sibling_category_members_browse_permission(sibling_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def category_thread(category):
    return post_thread(category, title="Category Thread")
