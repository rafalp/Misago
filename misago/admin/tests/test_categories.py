from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...categories.models import Category
from ...threads import test
from ...threads.models import Thread
from ...test import assert_contains
from ..test import AdminTestCase

categories_list = reverse("misago:admin:categories:index")


def test_categories_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(categories_list)
    assert_contains(response, categories_list)


def test_categories_list_renders(admin_client, default_category):
    response = admin_client.get(categories_list)
    assert_contains(response, default_category.name)


def test_categories_list_renders_empty_message(admin_client, root_category):
    for child in root_category.get_descendants():
        child.delete()

    response = admin_client.get(categories_list)
    assert_contains(response, "No categories are set.")


class CategoryAdminViewsTests(AdminTestCase):

    def test_list_view(self):
        """categories list view returns 200"""
        response = self.client.get(reverse("misago:admin:categories:index"))

        self.assertContains(response, "First category")

        # Now test that empty categories list contains message
        root = Category.objects.root_category()
        for descendant in root.get_descendants():
            descendant.delete()

        response = self.client.get(reverse("misago:admin:categories:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No categories")

    def test_new_view(self):
        """new category view has no showstoppers"""
        root = Category.objects.root_category()
        first_category = Category.objects.get(slug="first-category")

        response = self.client.get(reverse("misago:admin:categories:new"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Test Category",
                "description": "Lorem ipsum dolor met",
                "new_parent": root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:categories:index"))
        self.assertContains(response, "Test Category")

        test_category = Category.objects.get(slug="test-category")

        self.assertValidTree(
            [(root, 0, 1, 6), (first_category, 1, 2, 3), (test_category, 1, 4, 5)]
        )

        response = self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Test Other Category",
                "description": "Lorem ipsum dolor met",
                "new_parent": root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.assertEqual(response.status_code, 302)

        test_other_category = Category.objects.get(slug="test-other-category")

        self.assertValidTree(
            [
                (root, 0, 1, 8),
                (first_category, 1, 2, 3),
                (test_category, 1, 4, 5),
                (test_other_category, 1, 6, 7),
            ]
        )

        response = self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Test Subcategory",
                "new_parent": test_category.pk,
                "copy_permissions": test_category.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.assertEqual(response.status_code, 302)

        test_subcategory = Category.objects.get(slug="test-subcategory")

        self.assertValidTree(
            [
                (root, 0, 1, 10),
                (first_category, 1, 2, 3),
                (test_category, 1, 4, 7),
                (test_subcategory, 2, 5, 6),
                (test_other_category, 1, 8, 9),
            ]
        )

        response = self.client.get(reverse("misago:admin:categories:index"))
        self.assertContains(response, "Test Subcategory")

    def test_creating_new_category_invalidates_acl_cache(self):
        root = Category.objects.root_category()

        with assert_invalidates_cache(ACL_CACHE):
            self.client.post(
                reverse("misago:admin:categories:new"),
                data={
                    "name": "Test Category",
                    "description": "Lorem ipsum dolor met",
                    "new_parent": root.pk,
                    "prune_started_after": 0,
                    "prune_replied_after": 0,
                },
            )

    def test_edit_view(self):
        """edit category view has no showstoppers"""
        private_threads = Category.objects.private_threads()
        root = Category.objects.root_category()
        first_category = Category.objects.get(slug="first-category")

        response = self.client.get(
            reverse("misago:admin:categories:edit", kwargs={"pk": private_threads.pk})
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse("misago:admin:categories:edit", kwargs={"pk": root.pk})
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Test Category",
                "description": "Lorem ipsum dolor met",
                "new_parent": root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.assertEqual(response.status_code, 302)

        test_category = Category.objects.get(slug="test-category")

        response = self.client.get(
            reverse("misago:admin:categories:edit", kwargs={"pk": test_category.pk})
        )

        self.assertContains(response, "Test Category")

        response = self.client.post(
            reverse("misago:admin:categories:edit", kwargs={"pk": test_category.pk}),
            data={
                "name": "Test Category Edited",
                "new_parent": root.pk,
                "role": "category",
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.assertEqual(response.status_code, 302)

        self.assertValidTree(
            [(root, 0, 1, 6), (first_category, 1, 2, 3), (test_category, 1, 4, 5)]
        )

        response = self.client.get(reverse("misago:admin:categories:index"))
        self.assertContains(response, "Test Category Edited")

        response = self.client.post(
            reverse("misago:admin:categories:edit", kwargs={"pk": test_category.pk}),
            data={
                "name": "Test Category Edited",
                "new_parent": first_category.pk,
                "role": "category",
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.assertEqual(response.status_code, 302)

        self.assertValidTree(
            [(root, 0, 1, 6), (first_category, 1, 2, 5), (test_category, 2, 3, 4)]
        )

        response = self.client.get(reverse("misago:admin:categories:index"))
        self.assertContains(response, "Test Category Edited")

    def test_editing_category_invalidates_acl_cache(self):
        root = Category.objects.root_category()
        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Test Category",
                "description": "Lorem ipsum dolor met",
                "new_parent": root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )

        test_category = Category.objects.get(slug="test-category")

        with assert_invalidates_cache(ACL_CACHE):
            self.client.post(
                reverse(
                    "misago:admin:categories:edit", kwargs={"pk": test_category.pk}
                ),
                data={
                    "name": "Test Category Edited",
                    "new_parent": root.pk,
                    "role": "category",
                    "prune_started_after": 0,
                    "prune_replied_after": 0,
                },
            )

    def test_move_views(self):
        """move up/down views have no showstoppers"""
        root = Category.objects.root_category()
        first_category = Category.objects.get(slug="first-category")

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Category A",
                "new_parent": root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        category_a = Category.objects.get(slug="category-a")

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Category B",
                "new_parent": root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        category_b = Category.objects.get(slug="category-b")

        response = self.client.post(
            reverse("misago:admin:categories:up", kwargs={"pk": category_b.pk})
        )
        self.assertEqual(response.status_code, 302)

        self.assertValidTree(
            [
                (root, 0, 1, 8),
                (first_category, 1, 2, 3),
                (category_b, 1, 4, 5),
                (category_a, 1, 6, 7),
            ]
        )

        response = self.client.post(
            reverse("misago:admin:categories:up", kwargs={"pk": category_b.pk})
        )
        self.assertEqual(response.status_code, 302)

        self.assertValidTree(
            [
                (root, 0, 1, 8),
                (category_b, 1, 2, 3),
                (first_category, 1, 4, 5),
                (category_a, 1, 6, 7),
            ]
        )

        response = self.client.post(
            reverse("misago:admin:categories:down", kwargs={"pk": category_b.pk})
        )
        self.assertEqual(response.status_code, 302)

        self.assertValidTree(
            [
                (root, 0, 1, 8),
                (first_category, 1, 2, 3),
                (category_b, 1, 4, 5),
                (category_a, 1, 6, 7),
            ]
        )

        response = self.client.post(
            reverse("misago:admin:categories:down", kwargs={"pk": category_b.pk})
        )
        self.assertEqual(response.status_code, 302)

        self.assertValidTree(
            [
                (root, 0, 1, 8),
                (first_category, 1, 2, 3),
                (category_a, 1, 4, 5),
                (category_b, 1, 6, 7),
            ]
        )

        response = self.client.post(
            reverse("misago:admin:categories:down", kwargs={"pk": category_b.pk})
        )
        self.assertEqual(response.status_code, 302)

        self.assertValidTree(
            [
                (root, 0, 1, 8),
                (first_category, 1, 2, 3),
                (category_a, 1, 4, 5),
                (category_b, 1, 6, 7),
            ]
        )
