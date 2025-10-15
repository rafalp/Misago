from unittest.mock import patch

from django.urls import reverse

from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


def test_category_threads_list_returns_404_for_top_level_vanilla_category_without_children(
    default_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 404


def test_category_threads_list_returns_404_for_top_level_vanilla_category_with_invisible_children(
    default_category, child_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    CategoryGroupPermission.objects.filter(category=child_category).delete()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 404


def test_category_threads_list_renders_for_top_level_vanilla_category_with_children(
    default_category, child_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 200


def test_category_threads_list_renders_for_nested_vanilla_category_without_children(
    child_category, client
):
    child_category.is_vanilla = True
    child_category.list_children_threads = False
    child_category.save()

    response = client.get(child_category.get_absolute_url())
    assert response.status_code == 200
