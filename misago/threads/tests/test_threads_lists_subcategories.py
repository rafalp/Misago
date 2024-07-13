from django.urls import reverse

from ...categories.enums import CategoryChildrenComponent
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...test import assert_contains, assert_not_contains
from ...testutils import grant_category_group_permissions


@override_dynamic_settings(
    index_view="categories",
    threads_list_categories_component=CategoryChildrenComponent.DISABLED,
)
def test_threads_list_renders_no_subcategories_component(default_category, client):
    response = client.get(reverse("misago:threads"))
    assert_not_contains(response, "list-group-category")


@override_dynamic_settings(
    index_view="categories",
    threads_list_categories_component=CategoryChildrenComponent.FULL,
)
def test_threads_list_renders_full_subcategories_component(default_category, client):
    response = client.get(reverse("misago:threads"))
    assert_contains(response, default_category.name)
    assert_contains(response, "list-group-category")


@override_dynamic_settings(
    index_view="categories",
    threads_list_categories_component=CategoryChildrenComponent.DROPDOWN,
)
def test_threads_list_renders_dropdown_subcategories_component(
    default_category, client, guests_group
):
    default_category.children_categories_component = CategoryChildrenComponent.DROPDOWN
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        guests_group,
        CategoryPermission.SEE,
    )

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "dropdown-category")


def test_category_threads_list_renders_full_subcategories_component(
    default_category, client, guests_group
):
    default_category.children_categories_component = CategoryChildrenComponent.FULL
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        guests_group,
        CategoryPermission.SEE,
    )

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "list-group-category")


def test_category_threads_list_renders_dropdown_subcategories_component(
    default_category, client, guests_group
):
    default_category.children_categories_component = CategoryChildrenComponent.DROPDOWN
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        child_category,
        guests_group,
        CategoryPermission.SEE,
    )

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "dropdown-category")
