from django.urls import reverse

from ...categories.models import Category
from ...test import assert_contains

categories_list = reverse("misago:admin:categories:index")


def test_categories_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(categories_list)
    assert_contains(response, categories_list)


def test_categories_list_renders_empty(admin_client, root_category):
    for child in root_category.get_descendants():
        child.delete()

    response = admin_client.get(categories_list)
    assert_contains(response, "No categories are set.")


def test_categories_list_renders_category(admin_client, default_category):
    response = admin_client.get(categories_list)
    assert_contains(response, default_category.name)


def test_categories_list_renders_child_category(admin_client, default_category):
    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    response = admin_client.get(categories_list)
    assert_contains(response, child_category.name)
