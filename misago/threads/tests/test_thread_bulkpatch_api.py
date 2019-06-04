import json

from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ..models import Thread
from ..test import patch_category_acl, patch_other_category_acl
from .test_threads_api import ThreadsApiTestCase


class ThreadsBulkPatchApiTestCase(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.threads = list(
            reversed(
                [
                    test.post_thread(category=self.category),
                    test.post_thread(category=self.category),
                    test.post_thread(category=self.category),
                ]
            )
        )

        self.ids = list(reversed([t.id for t in self.threads]))

        self.api_link = reverse("misago:api:thread-list")

    def patch(self, api_link, ops):
        return self.client.patch(
            api_link, json.dumps(ops), content_type="application/json"
        )


class BulkPatchSerializerTests(ThreadsBulkPatchApiTestCase):
    def test_invalid_input_type(self):
        """api rejects invalid input type"""
        response = self.patch(self.api_link, [1, 2, 3])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got list."
                ]
            },
        )

    def test_missing_input_keys(self):
        """api rejects input with missing keys"""
        response = self.patch(self.api_link, {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"ids": ["This field is required."], "ops": ["This field is required."]},
        )

    def test_empty_input_keys(self):
        """api rejects input with empty keys"""
        response = self.patch(self.api_link, {"ids": [], "ops": []})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "ids": ["Ensure this field has at least 1 elements."],
                "ops": ["Ensure this field has at least 1 elements."],
            },
        )

    def test_invalid_input_keys(self):
        """api rejects input with invalid keys"""
        response = self.patch(self.api_link, {"ids": ["a"], "ops": [1]})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "ids": {"0": ["A valid integer is required."]},
                "ops": {"0": ['Expected a dictionary of items but got type "int".']},
            },
        )

    def test_too_small_id(self):
        """api rejects input with implausiple id"""
        response = self.patch(self.api_link, {"ids": [0], "ops": [{}]})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"ids": {"0": ["Ensure this value is greater than or equal to 1."]}},
        )

    @override_dynamic_settings(threads_per_page=5)
    def test_too_large_input(self):
        """api rejects too large input"""
        response = self.patch(
            self.api_link,
            {"ids": [i + 1 for i in range(6)], "ops": [{} for i in range(200)]},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "ids": ["No more than 5 threads can be updated at a single time."],
                "ops": ["Ensure this field has no more than 10 elements."],
            },
        )

    def test_threads_not_found(self):
        """api fails to find threads"""
        threads = [
            test.post_thread(category=self.category, is_hidden=True),
            test.post_thread(category=self.category, is_unapproved=True),
        ]

        response = self.patch(
            self.api_link, {"ids": [t.id for t in threads], "ops": [{}]}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more threads to update could not be found."},
        )

    def test_ops_invalid(self):
        """api validates descriptions"""
        response = self.patch(self.api_link, {"ids": self.ids[:1], "ops": [{}]})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), [{"id": self.ids[0], "detail": ["undefined op"]}]
        )

    def test_anonymous_user(self):
        """anonymous users can't use bulk actions"""
        self.logout_user()

        response = self.patch(self.api_link, {"ids": self.ids[:1], "ops": [{}]})
        self.assertEqual(response.status_code, 403)


class ThreadAddAclApiTests(ThreadsBulkPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds current threads acl to response"""
        response = self.patch(
            self.api_link,
            {"ids": self.ids, "ops": [{"op": "add", "path": "acl", "value": True}]},
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, thread in enumerate(self.threads):
            self.assertEqual(response_json[i]["id"], thread.id)
            self.assertTrue(response_json[i]["acl"])


class BulkThreadChangeTitleApiTests(ThreadsBulkPatchApiTestCase):
    @patch_category_acl({"can_edit_threads": 2})
    def test_change_thread_title(self):
        """api changes thread title and resyncs the category"""
        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [
                    {"op": "replace", "path": "title", "value": "Changed the title!"}
                ],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, thread in enumerate(self.threads):
            self.assertEqual(response_json[i]["id"], thread.id)
            self.assertEqual(response_json[i]["title"], "Changed the title!")

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertEqual(thread.title, "Changed the title!")

        category = Category.objects.get(pk=self.category.id)
        self.assertEqual(category.last_thread_title, "Changed the title!")

    @patch_category_acl({"can_edit_threads": 0})
    def test_change_thread_title_no_permission(self):
        """api validates permission to change title, returns errors"""
        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [
                    {"op": "replace", "path": "title", "value": "Changed the title!"}
                ],
            },
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, thread in enumerate(self.threads):
            self.assertEqual(response_json[i]["id"], thread.id)
            self.assertEqual(
                response_json[i]["detail"], ["You can't edit threads in this category."]
            )


class BulkThreadMoveApiTests(ThreadsBulkPatchApiTestCase):
    def setUp(self):
        super().setUp()

        Category(name="Other Category", slug="other-category").insert_at(
            self.category, position="last-child", save=True
        )
        self.other_category = Category.objects.get(slug="other-category")

    @patch_category_acl({"can_move_threads": True})
    @patch_other_category_acl({"can_start_threads": 2})
    def test_move_thread(self):
        """api moves threads to other category and syncs both categories"""
        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [
                    {
                        "op": "replace",
                        "path": "category",
                        "value": self.other_category.id,
                    },
                    {"op": "replace", "path": "flatten-categories", "value": None},
                ],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, thread in enumerate(self.threads):
            self.assertEqual(response_json[i]["id"], thread.id)
            self.assertEqual(response_json[i]["category"], self.other_category.id)

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertEqual(thread.category_id, self.other_category.id)

        category = Category.objects.get(pk=self.category.id)
        self.assertEqual(category.threads, self.category.threads - 3)

        new_category = Category.objects.get(pk=self.other_category.id)
        self.assertEqual(new_category.threads, 3)


class BulkThreadsHideApiTests(ThreadsBulkPatchApiTestCase):
    @patch_category_acl({"can_hide_threads": 1})
    def test_hide_thread(self):
        """api makes it possible to hide thread"""
        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [{"op": "replace", "path": "is-hidden", "value": True}],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, thread in enumerate(self.threads):
            self.assertEqual(response_json[i]["id"], thread.id)
            self.assertTrue(response_json[i]["is_hidden"])

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertTrue(thread.is_hidden)

        category = Category.objects.get(pk=self.category.id)
        self.assertNotIn(category.last_thread_id, self.ids)


class BulkThreadsApproveApiTests(ThreadsBulkPatchApiTestCase):
    @patch_category_acl({"can_approve_content": True})
    def test_approve_thread(self):
        """api approvse threads and syncs category"""
        for thread in self.threads:
            thread.first_post.is_unapproved = True
            thread.first_post.save()

            thread.synchronize()
            thread.save()

            self.assertTrue(thread.is_unapproved)
            self.assertTrue(thread.has_unapproved_posts)

        self.category.synchronize()
        self.category.save()

        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [{"op": "replace", "path": "is-unapproved", "value": False}],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, thread in enumerate(self.threads):
            self.assertEqual(response_json[i]["id"], thread.id)
            self.assertFalse(response_json[i]["is_unapproved"])
            self.assertFalse(response_json[i]["has_unapproved_posts"])

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertFalse(thread.is_unapproved)
            self.assertFalse(thread.has_unapproved_posts)

        category = Category.objects.get(pk=self.category.id)
        self.assertIn(category.last_thread_id, self.ids)
