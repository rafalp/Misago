from datetime import timedelta

from django.utils import timezone

from .. import test
from ...categories import THREADS_ROOT_NAME
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase
from ..models import Thread
from ..test import patch_category_acl
from ..threadtypes import trees_map


class ThreadsApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

        self.root = Category.objects.get(tree_id=threads_tree_id, level=0)
        self.category = Category.objects.get(slug="first-category")

        self.thread = test.post_thread(category=self.category)
        self.api_link = self.thread.get_api_url()

    def get_thread_json(self):
        response = self.client.get(self.thread.get_api_url())
        self.assertEqual(response.status_code, 200)

        return response.json()


class ThreadRetrieveApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.tested_links = [
            self.api_link,
            "%sposts/" % self.api_link,
            "%sposts/?page=1" % self.api_link,
        ]

    @patch_category_acl()
    def test_api_returns_thread(self):
        """api has no showstoppers"""
        for link in self.tested_links:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertEqual(response_json["id"], self.thread.pk)
            self.assertEqual(response_json["title"], self.thread.title)

            if "posts" in link:
                self.assertIn("post_set", response_json)

    @patch_category_acl({"can_see_all_threads": False})
    def test_api_shows_owned_thread(self):
        """api handles "owned threads only"""
        for link in self.tested_links:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

        self.thread.starter = self.user
        self.thread.save()

        for link in self.tested_links:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_see": False})
    def test_api_validates_category_see_permission(self):
        """api validates category visiblity"""
        for link in self.tested_links:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_browse": False})
    def test_api_validates_category_browse_permission(self):
        """api validates category browsability"""
        for link in self.tested_links:
            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

    def test_api_validates_posts_visibility(self):
        """api validates posts visiblity"""
        hidden_post = test.reply_thread(
            self.thread, is_hidden=True, message="I'am hidden test message!"
        )

        with patch_category_acl({"can_hide_posts": 0}):
            response = self.client.get(self.tested_links[1])
            self.assertNotContains(
                response, hidden_post.parsed
            )  # post's body is hidden

        # add permission to see hidden posts
        with patch_category_acl({"can_hide_posts": 1}):
            response = self.client.get(self.tested_links[1])
            self.assertContains(
                response, hidden_post.parsed
            )  # hidden post's body is visible with permission

        # unapproved posts shouldn't show at all
        unapproved_post = test.reply_thread(self.thread, is_unapproved=True)

        with patch_category_acl({"can_approve_content": False}):
            response = self.client.get(self.tested_links[1])
            self.assertNotContains(response, unapproved_post.get_absolute_url())

        # add permission to see unapproved posts
        with patch_category_acl({"can_approve_content": True}):
            response = self.client.get(self.tested_links[1])
            self.assertContains(response, unapproved_post.get_absolute_url())

    def test_api_validates_has_unapproved_posts_visibility(self):
        """api checks acl before exposing unapproved flag"""
        self.thread.has_unapproved_posts = True
        self.thread.save()

        with patch_category_acl({"can_approve_content": False}):
            for link in self.tested_links:
                response = self.client.get(link)
                self.assertEqual(response.status_code, 200)

                response_json = response.json()
                self.assertEqual(response_json["id"], self.thread.pk)
                self.assertEqual(response_json["title"], self.thread.title)
                self.assertFalse(response_json["has_unapproved_posts"])

        with patch_category_acl({"can_approve_content": True}):
            for link in self.tested_links:
                response = self.client.get(link)
                self.assertEqual(response.status_code, 200)

                response_json = response.json()
                self.assertEqual(response_json["id"], self.thread.pk)
                self.assertEqual(response_json["title"], self.thread.title)
                self.assertTrue(response_json["has_unapproved_posts"])


class ThreadDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.last_thread = test.post_thread(category=self.category)
        self.api_link = self.last_thread.get_api_url()

    def test_delete_thread_no_permission(self):
        """api tests permission to delete threads"""
        with patch_category_acl({"can_hide_threads": 0}):
            response = self.client.delete(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json()["detail"], "You can't delete threads in this category."
            )

        with patch_category_acl({"can_hide_threads": 1}):
            response = self.client.delete(self.api_link)
            self.assertEqual(response.status_code, 403)
            self.assertEqual(
                response.json()["detail"], "You can't delete threads in this category."
            )

    @patch_category_acl({"can_hide_threads": 1, "can_hide_own_threads": 2})
    def test_delete_other_user_thread_no_permission(self):
        """api tests thread owner when deleting own thread"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"],
            "You can't delete other users theads in this category.",
        )

    @patch_category_acl(
        {"can_hide_threads": 2, "can_hide_own_threads": 2, "can_close_threads": False}
    )
    def test_delete_thread_closed_category_no_permission(self):
        """api tests category's closed state"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"],
            "This category is closed. You can't delete threads in it.",
        )

    @patch_category_acl(
        {"can_hide_threads": 2, "can_hide_own_threads": 2, "can_close_threads": False}
    )
    def test_delete_thread_closed_no_permission(self):
        """api tests thread's closed state"""
        self.last_thread.is_closed = True
        self.last_thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"], "This thread is closed. You can't delete it."
        )

    @patch_category_acl(
        {"can_hide_threads": 1, "can_hide_own_threads": 2, "thread_edit_time": 1}
    )
    def test_delete_owned_thread_no_time(self):
        """api tests permission to delete owned thread within time limit"""
        self.last_thread.starter = self.user
        self.last_thread.started_on = timezone.now() - timedelta(minutes=10)
        self.last_thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"],
            "You can't delete threads that are older than 1 minute.",
        )

    @patch_category_acl({"can_hide_threads": 2})
    def test_delete_thread(self):
        """DELETE to API link with permission deletes thread"""
        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.last_thread_id, self.last_thread.pk)

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.last_thread.pk)

        # category was synchronised after deletion
        category = Category.objects.get(slug="first-category")
        self.assertEqual(category.last_thread_id, self.thread.pk)

        # test that last thread's deletion triggers category sync
        response = self.client.delete(self.thread.get_api_url())
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        category = Category.objects.get(slug="first-category")
        self.assertIsNone(category.last_thread_id)

    @patch_category_acl(
        {"can_hide_threads": 1, "can_hide_own_threads": 2, "thread_edit_time": 30}
    )
    def test_delete_owned_thread(self):
        """api lets owner to delete owned thread within time limit"""
        self.last_thread.starter = self.user
        self.last_thread.started_on = timezone.now() - timedelta(minutes=10)
        self.last_thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)
