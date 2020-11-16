import json

from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...users.test import AuthenticatedUserTestCase
from ..models import Post, Thread
from ..test import patch_category_acl


class ThreadPostBulkPatchApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)
        self.posts = [
            test.reply_thread(self.thread, poster=self.user),
            test.reply_thread(self.thread),
            test.reply_thread(self.thread, poster=self.user),
        ]

        self.ids = [p.id for p in self.posts]

        self.api_link = reverse(
            "misago:api:thread-post-list", kwargs={"thread_pk": self.thread.pk}
        )

    def patch(self, api_link, ops):
        return self.client.patch(
            api_link, json.dumps(ops), content_type="application/json"
        )


class BulkPatchSerializerTests(ThreadPostBulkPatchApiTestCase):
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

    @override_dynamic_settings(posts_per_page=4, posts_per_page_orphans=3)
    def test_too_large_input(self):
        """api rejects too large input"""
        response = self.patch(
            self.api_link,
            {"ids": [i + 1 for i in range(8)], "ops": [{} for i in range(200)]},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "ids": ["No more than 7 posts can be updated at a single time."],
                "ops": ["Ensure this field has no more than 10 elements."],
            },
        )

    def test_posts_not_found(self):
        """api fails to find posts"""
        posts = [
            test.reply_thread(self.thread, is_hidden=True),
            test.reply_thread(self.thread, is_unapproved=True),
        ]

        response = self.patch(
            self.api_link, {"ids": [p.id for p in posts], "ops": [{}]}
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to update could not be found."},
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

    def test_events(self):
        """cant use bulk actions for events"""
        for post in self.posts:
            post.is_event = True
            post.save()

        response = self.patch(self.api_link, {"ids": self.ids, "ops": [{}]})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to update could not be found."},
        )


class PostsAddAclApiTests(ThreadPostBulkPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds posts acls to response"""
        response = self.patch(
            self.api_link,
            {"ids": self.ids, "ops": [{"op": "add", "path": "acl", "value": True}]},
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]["id"], post.id)
            self.assertTrue(response_json[i]["acl"])


class BulkPostProtectApiTests(ThreadPostBulkPatchApiTestCase):
    @patch_category_acl({"can_protect_posts": True, "can_edit_posts": 2})
    def test_protect_post(self):
        """api makes it possible to protect posts"""
        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [{"op": "replace", "path": "is-protected", "value": True}],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]["id"], post.id)
            self.assertTrue(response_json[i]["is_protected"])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_protected)

    @patch_category_acl({"can_protect_posts": False})
    def test_protect_post_no_permission(self):
        """api validates permission to protect posts and returns errors"""
        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [{"op": "replace", "path": "is-protected", "value": True}],
            },
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]["id"], post.id)
            self.assertEqual(
                response_json[i]["detail"],
                ["You can't protect posts in this category."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_protected)


class BulkPostsApproveApiTests(ThreadPostBulkPatchApiTestCase):
    @patch_category_acl({"can_approve_content": True})
    def test_approve_post(self):
        """api resyncs thread and categories on posts approval"""
        for post in self.posts:
            post.is_unapproved = True
            post.save()

        self.thread.synchronize()
        self.thread.save()

        self.assertNotIn(self.thread.last_post_id, self.ids)

        response = self.patch(
            self.api_link,
            {
                "ids": self.ids,
                "ops": [{"op": "replace", "path": "is-unapproved", "value": False}],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]["id"], post.id)
            self.assertFalse(response_json[i]["is_unapproved"])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_unapproved)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertIn(thread.last_post_id, self.ids)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.posts, 4)
