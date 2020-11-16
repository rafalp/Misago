from django.urls import reverse

from ....acl import ACL_CACHE
from ....admin.test import AdminTestCase
from ....cache.test import assert_invalidates_cache
from ....threads import test
from ....threads.models import Thread
from ...models import Category


class CategoryAdminTestCase(AdminTestCase):
    def assertValidTree(self, expected_tree):
        root = Category.objects.root_category()
        queryset = Category.objects.filter(tree_id=root.tree_id).order_by("lft")

        current_tree = []
        for category in queryset:
            current_tree.append(
                (
                    category,
                    category.level,
                    category.lft - root.lft + 1,
                    category.rght - root.lft + 1,
                )
            )

        if len(expected_tree) != len(current_tree):
            self.fail(
                "nodes tree is %s items long, should be %s"
                % (len(current_tree), len(expected_tree))
            )

        for i, category in enumerate(expected_tree):
            _category = current_tree[i]
            if category[0] != _category[0]:
                self.fail(
                    ("expected category at index #%s to be %s, " "found %s instead")
                    % (i, category[0], _category[0])
                )
            if category[1] != _category[1]:
                self.fail(
                    ("expected level at index #%s to be %s, " "found %s instead")
                    % (i, category[1], _category[1])
                )
            if category[2] != _category[2]:
                self.fail(
                    ("expected lft at index #%s to be %s, " "found %s instead")
                    % (i, category[2], _category[2])
                )
            if category[3] != _category[3]:
                self.fail(
                    ("expected lft at index #%s to be %s, " "found %s instead")
                    % (i, category[3], _category[3])
                )


class CategoryAdminViewsTests(CategoryAdminTestCase):
    def test_link_registered(self):
        """admin nav contains categories link"""
        response = self.client.get(reverse("misago:admin:categories:index"))

        self.assertContains(response, reverse("misago:admin:categories:index"))

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


class CategoryAdminDeleteViewTests(CategoryAdminTestCase):
    def setUp(self):
        """
        Create categories tree for test cases:

        First category (created by migration)

        Category A
          + Category B
            + Subcategory C
            + Subcategory D

        Category E
          + Category F
        """

        super().setUp()

        self.root = Category.objects.root_category()
        self.first_category = Category.objects.get(slug="first-category")

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Category A",
                "new_parent": self.root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Category E",
                "new_parent": self.root.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )

        self.category_a = Category.objects.get(slug="category-a")
        self.category_e = Category.objects.get(slug="category-e")

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Category B",
                "new_parent": self.category_a.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.category_b = Category.objects.get(slug="category-b")

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Subcategory C",
                "new_parent": self.category_b.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.category_c = Category.objects.get(slug="subcategory-c")

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Subcategory D",
                "new_parent": self.category_b.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.category_d = Category.objects.get(slug="subcategory-d")

        self.client.post(
            reverse("misago:admin:categories:new"),
            data={
                "name": "Category F",
                "new_parent": self.category_e.pk,
                "prune_started_after": 0,
                "prune_replied_after": 0,
            },
        )
        self.category_f = Category.objects.get(slug="category-f")

    def test_delete_category_move_contents(self):
        """category was deleted and its contents were moved"""
        for _ in range(10):
            test.post_thread(self.category_b)
        self.assertEqual(Thread.objects.count(), 10)

        response = self.client.get(
            reverse("misago:admin:categories:delete", kwargs={"pk": self.category_b.pk})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse(
                "misago:admin:categories:delete", kwargs={"pk": self.category_b.pk}
            ),
            data={
                "move_children_to": self.category_e.pk,
                "move_threads_to": self.category_d.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.all_categories().count(), 6)
        self.assertEqual(Thread.objects.count(), 10)
        for thread in Thread.objects.all():
            self.assertEqual(thread.category_id, self.category_d.pk)

        self.assertValidTree(
            [
                (self.root, 0, 1, 14),
                (self.first_category, 1, 2, 3),
                (self.category_a, 1, 4, 5),
                (self.category_e, 1, 6, 13),
                (self.category_f, 2, 7, 8),
                (self.category_c, 2, 9, 10),
                (self.category_d, 2, 11, 12),
            ]
        )

    def test_delete_category_and_contents(self):
        """category and its contents were deleted"""
        for _ in range(10):
            test.post_thread(self.category_b)

        response = self.client.get(
            reverse("misago:admin:categories:delete", kwargs={"pk": self.category_b.pk})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse(
                "misago:admin:categories:delete", kwargs={"pk": self.category_b.pk}
            ),
            data={"move_children_to": "", "move_threads_to": ""},
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Category.objects.all_categories().count(), 4)
        self.assertEqual(Thread.objects.count(), 0)

        self.assertValidTree(
            [
                (self.root, 0, 1, 10),
                (self.first_category, 1, 2, 3),
                (self.category_a, 1, 4, 5),
                (self.category_e, 1, 6, 9),
                (self.category_f, 2, 7, 8),
            ]
        )

    def test_delete_leaf_category_and_contents(self):
        """leaf category was deleted with contents"""
        for _ in range(10):
            test.post_thread(self.category_d)
        self.assertEqual(Thread.objects.count(), 10)

        response = self.client.get(
            reverse("misago:admin:categories:delete", kwargs={"pk": self.category_d.pk})
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse(
                "misago:admin:categories:delete", kwargs={"pk": self.category_d.pk}
            ),
            data={"move_children_to": "", "move_threads_to": ""},
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Category.objects.all_categories().count(), 6)
        self.assertEqual(Thread.objects.count(), 0)

        self.assertValidTree(
            [
                (self.root, 0, 1, 14),
                (self.first_category, 1, 2, 3),
                (self.category_a, 1, 4, 9),
                (self.category_b, 2, 5, 8),
                (self.category_c, 3, 6, 7),
                (self.category_e, 1, 10, 13),
                (self.category_f, 2, 11, 12),
            ]
        )

    def test_deleting_category_invalidates_acl_cache(self):
        with assert_invalidates_cache(ACL_CACHE):
            self.client.post(
                reverse(
                    "misago:admin:categories:delete", kwargs={"pk": self.category_d.pk}
                ),
                data={"move_children_to": "", "move_threads_to": ""},
            )
