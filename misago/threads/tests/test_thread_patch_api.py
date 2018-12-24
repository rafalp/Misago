import json
from datetime import timedelta

from django.utils import timezone

from .. import test
from ...categories.models import Category
from ...readtracker import poststracker
from ..models import Thread
from ..test import patch_category_acl, patch_other_category_acl
from .test_threads_api import ThreadsApiTestCase


class ThreadPatchApiTestCase(ThreadsApiTestCase):
    def patch(self, api_link, ops):
        return self.client.patch(
            api_link, json.dumps(ops), content_type="application/json"
        )


class ThreadAddAclApiTests(ThreadPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds current thread's acl to response"""
        response = self.patch(
            self.api_link, [{"op": "add", "path": "acl", "value": True}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertTrue(response_json["acl"])

    def test_add_acl_false(self):
        """
        if value is false, api won't add acl to the response, but will set empty key
        """
        response = self.patch(
            self.api_link, [{"op": "add", "path": "acl", "value": False}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIsNone(response_json["acl"])


class ThreadChangeTitleApiTests(ThreadPatchApiTestCase):
    @patch_category_acl({"can_edit_threads": 2})
    def test_change_thread_title(self):
        """api makes it possible to change thread title"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "title", "value": "Lorem ipsum change!"}],
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["title"], "Lorem ipsum change!")

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["title"], "Lorem ipsum change!")

    @patch_category_acl({"can_edit_threads": 0})
    def test_change_thread_title_no_permission(self):
        """api validates permission to change title"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "title", "value": "Lorem ipsum change!"}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "You can't edit threads in this category."
        )

    @patch_category_acl({"can_edit_threads": 2, "can_close_threads": 0})
    def test_change_thread_title_closed_category_no_permission(self):
        """api test permission to edit thread title in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "title", "value": "Lorem ipsum change!"}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "This category is closed. You can't edit threads in it.",
        )

    @patch_category_acl({"can_edit_threads": 2, "can_close_threads": 0})
    def test_change_thread_title_closed_thread_no_permission(self):
        """api test permission to edit closed thread title"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "title", "value": "Lorem ipsum change!"}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "This thread is closed. You can't edit it."
        )

    @patch_category_acl({"can_edit_threads": 1, "thread_edit_time": 1})
    def test_change_thread_title_after_edit_time(self):
        """api cleans, validates and rejects too short title"""
        self.thread.started_on = timezone.now() - timedelta(minutes=10)
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "title", "value": "Lorem ipsum change!"}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't edit threads that are older than 1 minute.",
        )

    @patch_category_acl({"can_edit_threads": 2})
    def test_change_thread_title_invalid(self):
        """api cleans, validates and rejects too short title"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "title", "value": 12}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "Thread title should be at least 5 characters long (it has 2).",
        )


class ThreadPinGloballyApiTests(ThreadPatchApiTestCase):
    @patch_category_acl({"can_pin_threads": 2})
    def test_pin_thread(self):
        """api makes it possible to pin globally thread"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 2}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["weight"], 2)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 2)

    @patch_category_acl({"can_pin_threads": 2, "can_close_threads": 0})
    def test_pin_thread_closed_category_no_permission(self):
        """api checks if category is closed"""
        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 2}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "This category is closed. You can't change threads weights in it.",
        )

    @patch_category_acl({"can_pin_threads": 2, "can_close_threads": 0})
    def test_pin_thread_closed_no_permission(self):
        """api checks if thread is closed"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 2}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "This thread is closed. You can't change its weight.",
        )

    @patch_category_acl({"can_pin_threads": 2})
    def test_unpin_thread(self):
        """api makes it possible to unpin thread"""
        self.thread.weight = 2
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 2)

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 0}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["weight"], 0)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 0)

    @patch_category_acl({"can_pin_threads": 1})
    def test_pin_thread_no_permission(self):
        """api pin thread globally with no permission fails"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 2}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't pin threads globally in this category.",
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 0)

    @patch_category_acl({"can_pin_threads": 1})
    def test_unpin_thread_no_permission(self):
        """api unpin thread with no permission fails"""
        self.thread.weight = 2
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 2)

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 1}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't change globally pinned threads weights in this category.",
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 2)


class ThreadPinLocallyApiTests(ThreadPatchApiTestCase):
    @patch_category_acl({"can_pin_threads": 1})
    def test_pin_thread(self):
        """api makes it possible to pin locally thread"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 1}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["weight"], 1)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 1)

    @patch_category_acl({"can_pin_threads": 1})
    def test_unpin_thread(self):
        """api makes it possible to unpin thread"""
        self.thread.weight = 1
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 1)

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 0}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["weight"], 0)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 0)

    @patch_category_acl({"can_pin_threads": 0})
    def test_pin_thread_no_permission(self):
        """api pin thread locally with no permission fails"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 1}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't change threads weights in this category.",
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 0)

    @patch_category_acl({"can_pin_threads": 0})
    def test_unpin_thread_no_permission(self):
        """api unpin thread with no permission fails"""
        self.thread.weight = 1
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 1)

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "weight", "value": 0}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't change threads weights in this category.",
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["weight"], 1)


class ThreadMoveApiTests(ThreadPatchApiTestCase):
    def setUp(self):
        super().setUp()

        Category(name="Other category", slug="other-category").insert_at(
            self.category, position="last-child", save=True
        )
        self.dst_category = Category.objects.get(slug="other-category")

    @patch_other_category_acl({"can_start_threads": 2})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_no_top(self):
        """api moves thread to other category, sets no top category"""
        response = self.patch(
            self.api_link,
            [
                {"op": "replace", "path": "category", "value": self.dst_category.pk},
                {"op": "add", "path": "top-category", "value": self.dst_category.pk},
                {"op": "replace", "path": "flatten-categories", "value": None},
            ],
        )
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertEqual(reponse_json["category"], self.dst_category.pk)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["category"]["id"], self.dst_category.pk)

    @patch_other_category_acl({"can_start_threads": 2})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_with_top(self):
        """api moves thread to other category, sets top"""
        response = self.patch(
            self.api_link,
            [
                {"op": "replace", "path": "category", "value": self.dst_category.pk},
                {
                    "op": "add",
                    "path": "top-category",
                    "value": Category.objects.root_category().pk,
                },
                {"op": "replace", "path": "flatten-categories", "value": None},
            ],
        )
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertEqual(reponse_json["category"], self.dst_category.pk)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["category"]["id"], self.dst_category.pk)

    @patch_other_category_acl({"can_start_threads": 2})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_reads(self):
        """api moves thread reads together with thread"""
        poststracker.save_read(self.user, self.thread.first_post)

        self.assertEqual(self.user.postread_set.count(), 1)
        self.user.postread_set.get(category=self.category)

        response = self.patch(
            self.api_link,
            [
                {"op": "replace", "path": "category", "value": self.dst_category.pk},
                {"op": "add", "path": "top-category", "value": self.dst_category.pk},
                {"op": "replace", "path": "flatten-categories", "value": None},
            ],
        )
        self.assertEqual(response.status_code, 200)

        # thread read was moved to new category
        postreads = self.user.postread_set.filter(post__is_event=False).order_by("id")

        self.assertEqual(postreads.count(), 1)
        postreads.get(category=self.dst_category)

    @patch_other_category_acl({"can_start_threads": 2})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_subscriptions(self):
        """api moves thread subscriptions together with thread"""
        self.user.subscription_set.create(
            thread=self.thread,
            category=self.thread.category,
            last_read_on=self.thread.last_post_on,
            send_email=False,
        )

        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(category=self.category)

        response = self.patch(
            self.api_link,
            [
                {"op": "replace", "path": "category", "value": self.dst_category.pk},
                {"op": "add", "path": "top-category", "value": self.dst_category.pk},
                {"op": "replace", "path": "flatten-categories", "value": None},
            ],
        )
        self.assertEqual(response.status_code, 200)

        # thread read was moved to new category
        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(category=self.dst_category)

    @patch_category_acl({"can_move_threads": False})
    def test_move_thread_no_permission(self):
        """api move thread to other category with no permission fails"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "category", "value": self.dst_category.pk}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "You can't move threads in this category."
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["category"]["id"], self.category.pk)

    @patch_other_category_acl({"can_close_threads": False})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_closed_category_no_permission(self):
        """api move thread from closed category with no permission fails"""
        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "category", "value": self.dst_category.pk}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "This category is closed. You can't move it's threads.",
        )

    @patch_other_category_acl({"can_close_threads": False})
    @patch_category_acl({"can_move_threads": True})
    def test_move_closed_thread_no_permission(self):
        """api move closed thread with no permission fails"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "category", "value": self.dst_category.pk}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "This thread is closed. You can't move it."
        )

    @patch_other_category_acl({"can_see": False})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_no_category_access(self):
        """api move thread to category with no access fails"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "category", "value": self.dst_category.pk}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json["detail"][0], "NOT FOUND")

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["category"]["id"], self.category.pk)

    @patch_other_category_acl({"can_browse": False})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_no_category_browse(self):
        """api move thread to category with no browsing access fails"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "category", "value": self.dst_category.pk}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            'You don\'t have permission to browse "Other category" contents.',
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["category"]["id"], self.category.pk)

    @patch_other_category_acl({"can_start_threads": False})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_no_category_start_threads(self):
        """api move thread to category with no posting access fails"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "category", "value": self.dst_category.pk}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You don't have permission to start new threads in this category.",
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["category"]["id"], self.category.pk)

    @patch_other_category_acl({"can_start_threads": 2})
    @patch_category_acl({"can_move_threads": True})
    def test_move_thread_same_category(self):
        """api move thread to category it's already in fails"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "category", "value": self.thread.category_id}],
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't move thread to the category it's already in.",
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["category"]["id"], self.category.pk)

    def test_thread_flatten_categories(self):
        """api flatten thread categories"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "flatten-categories", "value": None}],
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["category"], self.category.pk)


class ThreadCloseApiTests(ThreadPatchApiTestCase):
    @patch_category_acl({"can_close_threads": True})
    def test_close_thread(self):
        """api makes it possible to close thread"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-closed", "value": True}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertTrue(response_json["is_closed"])

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json["is_closed"])

    @patch_category_acl({"can_close_threads": True})
    def test_open_thread(self):
        """api makes it possible to open thread"""
        self.thread.is_closed = True
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json["is_closed"])

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-closed", "value": False}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertFalse(response_json["is_closed"])

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json["is_closed"])

    @patch_category_acl({"can_close_threads": False})
    def test_close_thread_no_permission(self):
        """api close thread with no permission fails"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-closed", "value": True}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You don't have permission to close this thread.",
        )

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json["is_closed"])

    @patch_category_acl({"can_close_threads": False})
    def test_open_thread_no_permission(self):
        """api open thread with no permission fails"""
        self.thread.is_closed = True
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json["is_closed"])

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-closed", "value": False}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "You don't have permission to open this thread."
        )

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json["is_closed"])


class ThreadApproveApiTests(ThreadPatchApiTestCase):
    @patch_category_acl({"can_approve_content": True})
    def test_approve_thread(self):
        """api makes it possible to approve thread"""
        self.thread.first_post.is_unapproved = True
        self.thread.first_post.save()

        self.thread.synchronize()
        self.thread.save()

        self.assertTrue(self.thread.is_unapproved)
        self.assertTrue(self.thread.has_unapproved_posts)

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-unapproved", "value": False}]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertFalse(response_json["is_unapproved"])
        self.assertFalse(response_json["has_unapproved_posts"])

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json["is_unapproved"])
        self.assertFalse(thread_json["has_unapproved_posts"])

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.is_unapproved)
        self.assertFalse(thread.has_unapproved_posts)

    @patch_category_acl({"can_approve_content": True, "can_close_threads": False})
    def test_approve_thread_category_closed_no_permission(self):
        """api checks permission for approving threads in closed categories"""
        self.thread.first_post.is_unapproved = True
        self.thread.first_post.save()

        self.thread.synchronize()
        self.thread.save()

        self.assertTrue(self.thread.is_unapproved)
        self.assertTrue(self.thread.has_unapproved_posts)

        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-unapproved", "value": False}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "This category is closed. You can't approve threads in it.",
        )

    @patch_category_acl({"can_approve_content": True, "can_close_threads": False})
    def test_approve_thread_closed_no_permission(self):
        """api checks permission for approving posts in closed categories"""
        self.thread.first_post.is_unapproved = True
        self.thread.first_post.save()

        self.thread.synchronize()
        self.thread.save()

        self.assertTrue(self.thread.is_unapproved)
        self.assertTrue(self.thread.has_unapproved_posts)

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-unapproved", "value": False}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "This thread is closed. You can't approve it."
        )

    @patch_category_acl({"can_approve_content": True})
    def test_unapprove_thread(self):
        """api returns permission error on approval removal"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-unapproved", "value": True}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "Content approval can't be reversed."
        )


class ThreadHideApiTests(ThreadPatchApiTestCase):
    @patch_category_acl({"can_hide_threads": True})
    def test_hide_thread(self):
        """api makes it possible to hide thread"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": True}]
        )
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertTrue(reponse_json["is_hidden"])

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json["is_hidden"])

    @patch_category_acl({"can_hide_threads": False})
    def test_hide_thread_no_permission(self):
        """api hide thread with no permission fails"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": True}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "You can't hide threads in this category."
        )

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json["is_hidden"])

    @patch_category_acl({"can_hide_threads": False, "can_hide_own_threads": True})
    def test_hide_non_owned_thread(self):
        """api forbids non-moderator from hiding other users threads"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": True}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't hide other users theads in this category.",
        )

    @patch_category_acl(
        {"can_hide_threads": False, "can_hide_own_threads": True, "thread_edit_time": 1}
    )
    def test_hide_owned_thread_no_time(self):
        """api forbids non-moderator from hiding other users threads"""
        self.thread.started_on = timezone.now() - timedelta(minutes=5)
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": True}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "You can't hide threads that are older than 1 minute.",
        )

    @patch_category_acl({"can_hide_threads": True, "can_close_threads": False})
    def test_hide_closed_category_no_permission(self):
        """api test permission to hide thread in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": True}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "This category is closed. You can't hide threads in it.",
        )

    @patch_category_acl({"can_hide_threads": True, "can_close_threads": False})
    def test_hide_closed_thread_no_permission(self):
        """api test permission to hide closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": True}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "This thread is closed. You can't hide it."
        )


class ThreadUnhideApiTests(ThreadPatchApiTestCase):
    def setUp(self):
        super().setUp()

        self.thread.is_hidden = True
        self.thread.save()

    @patch_category_acl({"can_hide_threads": True})
    def test_unhide_thread(self):
        """api makes it possible to unhide thread"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": False}]
        )
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertFalse(reponse_json["is_hidden"])

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json["is_hidden"])

    @patch_category_acl({"can_hide_threads": False})
    def test_unhide_thread_no_permission(self):
        """api unhide thread with no permission fails as thread is invisible"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": True}]
        )
        self.assertEqual(response.status_code, 404)

    @patch_category_acl({"can_hide_threads": True, "can_close_threads": False})
    def test_unhide_closed_category_no_permission(self):
        """api test permission to unhide thread in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": False}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0],
            "This category is closed. You can't reveal threads in it.",
        )

    @patch_category_acl({"can_hide_threads": True, "can_close_threads": False})
    def test_unhide_closed_thread_no_permission(self):
        """api test permission to unhide closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "is-hidden", "value": False}]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["detail"][0], "This thread is closed. You can't reveal it."
        )


class ThreadSubscribeApiTests(ThreadPatchApiTestCase):
    def test_subscribe_thread(self):
        """api makes it possible to subscribe thread"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "subscription", "value": "notify"}],
        )

        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertFalse(reponse_json["subscription"])

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json["subscription"])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertFalse(subscription.send_email)

    def test_subscribe_thread_with_email(self):
        """api makes it possible to subscribe thread with emails"""
        response = self.patch(
            self.api_link, [{"op": "replace", "path": "subscription", "value": "email"}]
        )

        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertTrue(reponse_json["subscription"])

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json["subscription"])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertTrue(subscription.send_email)

    def test_unsubscribe_thread(self):
        """api makes it possible to unsubscribe thread"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "subscription", "value": "remove"}],
        )

        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIsNone(reponse_json["subscription"])

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["subscription"])

        self.assertEqual(self.user.subscription_set.count(), 0)

    def test_subscribe_as_guest(self):
        """api makes it impossible to subscribe thread"""
        self.logout_user()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "subscription", "value": "email"}]
        )

        self.assertEqual(response.status_code, 403)

    def test_subscribe_nonexistant_thread(self):
        """api makes it impossible to subscribe nonexistant thread"""
        bad_api_link = self.api_link.replace(
            str(self.thread.pk), str(self.thread.pk + 9)
        )

        response = self.patch(
            bad_api_link, [{"op": "replace", "path": "subscription", "value": "email"}]
        )

        self.assertEqual(response.status_code, 404)


class ThreadMarkBestAnswerApiTests(ThreadPatchApiTestCase):
    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer(self):
        """api makes it possible to mark best answer"""
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["ok"],
                "best_answer": best_answer.id,
                "best_answer_is_protected": False,
                "best_answer_marked_on": response.json()["best_answer_marked_on"],
                "best_answer_marked_by": self.user.id,
                "best_answer_marked_by_name": self.user.username,
                "best_answer_marked_by_slug": self.user.slug,
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], best_answer.id)
        self.assertEqual(thread_json["best_answer_is_protected"], False)
        self.assertEqual(
            thread_json["best_answer_marked_on"],
            response.json()["best_answer_marked_on"],
        )
        self.assertEqual(thread_json["best_answer_marked_by"], self.user.id)
        self.assertEqual(thread_json["best_answer_marked_by_name"], self.user.username)
        self.assertEqual(thread_json["best_answer_marked_by_slug"], self.user.slug)

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_anonymous(self):
        """api validates that user is authenticated before marking best answer"""
        self.logout_user()

        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 0})
    def test_mark_best_answer_no_permission(self):
        """api validates permission to mark best answers"""
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to mark best answers "
                    'in the "First category" category.'
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 1})
    def test_mark_best_answer_not_thread_starter(self):
        """api validates permission to mark best answers in owned thread"""
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to mark best answer in this thread "
                    "because you didn't start it."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

        # passing scenario is possible
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_mark_best_answers": 2, "can_close_threads": False})
    def test_mark_best_answer_category_closed_no_permission(self):
        """api validates permission to mark best answers in closed category"""
        best_answer = test.reply_thread(self.thread)

        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to mark best answer in this thread "
                    'because its category "First category" is closed.'
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2, "can_close_threads": True})
    def test_mark_best_answer_category_closed(self):
        """api validates permission to mark best answers in closed category"""
        best_answer = test.reply_thread(self.thread)

        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_mark_best_answers": 2, "can_close_threads": False})
    def test_mark_best_answer_thread_closed_no_permission(self):
        """api validates permission to mark best answers in closed thread"""
        best_answer = test.reply_thread(self.thread)

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You can't mark best answer in this thread because it's closed and "
                    "you don't have permission to open it."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2, "can_close_threads": True})
    def test_mark_best_answer_thread_closed(self):
        """api validates permission to mark best answers in closed thread"""
        best_answer = test.reply_thread(self.thread)

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_invalid_post_id(self):
        """api validates that post id is int"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": "d7sd89a7d98sa"}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.id, "detail": ["A valid integer is required."]},
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_post_not_found(self):
        """api validates that post exists"""
        response = self.patch(
            self.api_link,
            [
                {
                    "op": "replace",
                    "path": "best-answer",
                    "value": self.thread.last_post_id + 1,
                }
            ],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"id": self.thread.id, "detail": ["NOT FOUND"]}
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_post_invisible(self):
        """api validates post visibility to action author"""
        unapproved_post = test.reply_thread(self.thread, is_unapproved=True)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": unapproved_post.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"id": self.thread.id, "detail": ["NOT FOUND"]}
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_post_other_thread(self):
        """api validates post belongs to same thread"""
        other_thread = test.post_thread(self.category)

        response = self.patch(
            self.api_link,
            [
                {
                    "op": "replace",
                    "path": "best-answer",
                    "value": other_thread.first_post_id,
                }
            ],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"id": self.thread.id, "detail": ["NOT FOUND"]}
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_event_id(self):
        """api validates that post is not an event"""
        best_answer = test.reply_thread(self.thread)
        best_answer.is_event = True
        best_answer.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["Events can't be marked as best answers."],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_first_post(self):
        """api validates that post is not a first post in thread"""
        response = self.patch(
            self.api_link,
            [
                {
                    "op": "replace",
                    "path": "best-answer",
                    "value": self.thread.first_post_id,
                }
            ],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["First post in a thread can't be marked as best answer."],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_hidden_post(self):
        """api validates that post is not hidden"""
        best_answer = test.reply_thread(self.thread, is_hidden=True)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["Hidden posts can't be marked as best answers."],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2})
    def test_mark_best_answer_unapproved_post(self):
        """api validates that post is not unapproved"""
        best_answer = test.reply_thread(
            self.thread, poster=self.user, is_unapproved=True
        )

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["Unapproved posts can't be marked as best answers."],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2, "can_protect_posts": False})
    def test_mark_best_answer_protected_post_no_permission(self):
        """api respects post protection"""
        best_answer = test.reply_thread(self.thread, is_protected=True)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to mark this post as best answer "
                    "because a moderator has protected it."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])

    @patch_category_acl({"can_mark_best_answers": 2, "can_protect_posts": True})
    def test_mark_best_answer_protected_post(self):
        """api respects post protection"""
        best_answer = test.reply_thread(self.thread, is_protected=True)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)


class ThreadChangeBestAnswerApiTests(ThreadPatchApiTestCase):
    def setUp(self):
        super().setUp()

        self.best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, self.best_answer)
        self.thread.save()

    @patch_category_acl({"can_mark_best_answers": 2, "can_change_marked_answers": 2})
    def test_change_best_answer(self):
        """api makes it possible to change best answer"""
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["ok"],
                "best_answer": best_answer.id,
                "best_answer_is_protected": False,
                "best_answer_marked_on": response.json()["best_answer_marked_on"],
                "best_answer_marked_by": self.user.id,
                "best_answer_marked_by_name": self.user.username,
                "best_answer_marked_by_slug": self.user.slug,
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], best_answer.id)
        self.assertEqual(thread_json["best_answer_is_protected"], False)
        self.assertEqual(
            thread_json["best_answer_marked_on"],
            response.json()["best_answer_marked_on"],
        )
        self.assertEqual(thread_json["best_answer_marked_by"], self.user.id)
        self.assertEqual(thread_json["best_answer_marked_by_name"], self.user.username)
        self.assertEqual(thread_json["best_answer_marked_by_slug"], self.user.slug)

    @patch_category_acl({"can_mark_best_answers": 2, "can_change_marked_answers": 2})
    def test_change_best_answer_same_post(self):
        """api validates if new best answer is same as current one"""
        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["This post is already marked as thread's best answer."],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl({"can_mark_best_answers": 0, "can_change_marked_answers": 2})
    def test_change_best_answer_no_permission_to_mark(self):
        """
        api validates permission to mark best answers before allowing answer change
        """
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to mark best answers in the "
                    '"First category" category.'
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl({"can_mark_best_answers": 2, "can_change_marked_answers": 0})
    def test_change_best_answer_no_permission(self):
        """api validates permission to change best answers"""
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to change this thread's marked answer "
                    'because it\'s in the "First category" category.'
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl({"can_mark_best_answers": 2, "can_change_marked_answers": 1})
    def test_change_best_answer_not_starter(self):
        """api validates permission to change best answers"""
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to change this thread's marked answer "
                    "because you are not a thread starter."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

        # passing scenario is possible
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl(
        {
            "can_mark_best_answers": 2,
            "can_change_marked_answers": 1,
            "best_answer_change_time": 5,
        }
    )
    def test_change_best_answer_timelimit_out_of_time(self):
        """
        api validates permission for starter to change best answers within timelimit
        """
        best_answer = test.reply_thread(self.thread)

        self.thread.best_answer_marked_on = timezone.now() - timedelta(minutes=6)
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to change best answer that was marked "
                    "for more than 5 minutes."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl(
        {
            "can_mark_best_answers": 2,
            "can_change_marked_answers": 1,
            "best_answer_change_time": 5,
        }
    )
    def test_change_best_answer_timelimit(self):
        """
        api validates permission for starter to change best answers within timelimit
        """
        best_answer = test.reply_thread(self.thread)

        self.thread.best_answer_marked_on = timezone.now() - timedelta(minutes=1)
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl(
        {
            "can_mark_best_answers": 2,
            "can_change_marked_answers": 2,
            "can_protect_posts": False,
        }
    )
    def test_change_best_answer_protected_no_permission(self):
        """api validates permission to change protected best answers"""
        best_answer = test.reply_thread(self.thread)

        self.thread.best_answer_is_protected = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to change this thread's best answer "
                    "because a moderator has protected it."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl(
        {
            "can_mark_best_answers": 2,
            "can_change_marked_answers": 2,
            "can_protect_posts": True,
        }
    )
    def test_change_best_answer_protected(self):
        """api validates permission to change protected best answers"""
        best_answer = test.reply_thread(self.thread)

        self.thread.best_answer_is_protected = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_mark_best_answers": 2, "can_change_marked_answers": 2})
    def test_change_best_answer_post_validation(self):
        """api validates new post'"""
        best_answer = test.reply_thread(self.thread, is_hidden=True)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)


class ThreadUnmarkBestAnswerApiTests(ThreadPatchApiTestCase):
    def setUp(self):
        super().setUp()

        self.best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, self.best_answer)
        self.thread.save()

    @patch_category_acl({"can_mark_best_answers": 0, "can_change_marked_answers": 2})
    def test_unmark_best_answer(self):
        """api makes it possible to unmark best answer"""
        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": ["ok"],
                "best_answer": None,
                "best_answer_is_protected": False,
                "best_answer_marked_on": None,
                "best_answer_marked_by": None,
                "best_answer_marked_by_name": None,
                "best_answer_marked_by_slug": None,
            },
        )

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json["best_answer"])
        self.assertFalse(thread_json["best_answer_is_protected"])
        self.assertIsNone(thread_json["best_answer_marked_on"])
        self.assertIsNone(thread_json["best_answer_marked_by"])
        self.assertIsNone(thread_json["best_answer_marked_by_name"])
        self.assertIsNone(thread_json["best_answer_marked_by_slug"])

    @patch_category_acl({"can_mark_best_answers": 0, "can_change_marked_answers": 2})
    def test_unmark_best_answer_invalid_post_id(self):
        """api validates that post id is int"""
        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": "d7sd89a7d98sa"}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.id, "detail": ["A valid integer is required."]},
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl({"can_mark_best_answers": 0, "can_change_marked_answers": 2})
    def test_unmark_best_answer_post_not_found(self):
        """api validates that post to unmark exists"""
        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id + 1}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"id": self.thread.id, "detail": ["NOT FOUND"]}
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl({"can_mark_best_answers": 0, "can_change_marked_answers": 2})
    def test_unmark_best_answer_wrong_post(self):
        """api validates if post given to unmark is best answer"""
        best_answer = test.reply_thread(self.thread)

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "This post can't be unmarked because it's not currently marked "
                    "as best answer."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl({"can_mark_best_answers": 0, "can_change_marked_answers": 0})
    def test_unmark_best_answer_no_permission(self):
        """api validates if user has permission to unmark best answers"""
        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to unmark threads answers in "
                    'the "First category" category.'
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl({"can_mark_best_answers": 0, "can_change_marked_answers": 1})
    def test_unmark_best_answer_not_starter(self):
        """api validates if starter has permission to unmark best answers"""
        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to unmark this best answer because "
                    "you are not a thread starter."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

        # passing scenario is possible
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl(
        {
            "can_mark_best_answers": 0,
            "can_change_marked_answers": 1,
            "best_answer_change_time": 5,
        }
    )
    def test_unmark_best_answer_timelimit(self):
        """
        api validates if starter has permission to unmark best answer within time limit
        """
        self.thread.best_answer_marked_on = timezone.now() - timedelta(minutes=6)
        self.thread.starter = self.user
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to unmark best answer that was marked "
                    "for more than 5 minutes."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

        # passing scenario is possible
        self.thread.best_answer_marked_on = timezone.now() - timedelta(minutes=2)
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl(
        {
            "can_mark_best_answers": 0,
            "can_change_marked_answers": 2,
            "can_close_threads": False,
        }
    )
    def test_unmark_best_answer_closed_category_no_permission(self):
        """
        api validates if user has permission to unmark best answer in closed category
        """
        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to unmark this best answer because "
                    'its category "First category" is closed.'
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl(
        {
            "can_mark_best_answers": 0,
            "can_change_marked_answers": 2,
            "can_close_threads": True,
        }
    )
    def test_unmark_best_answer_closed_category(self):
        """
        api validates if user has permission to unmark best answer in closed category
        """
        self.category.is_closed = True
        self.category.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl(
        {
            "can_mark_best_answers": 0,
            "can_change_marked_answers": 2,
            "can_close_threads": False,
        }
    )
    def test_unmark_best_answer_closed_thread_no_permission(self):
        """
        api validates if user has permission to unmark best answer in closed thread
        """
        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You can't unmark this thread's best answer because it's closed "
                    "and you don't have permission to open it."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl(
        {
            "can_mark_best_answers": 0,
            "can_change_marked_answers": 2,
            "can_close_threads": True,
        }
    )
    def test_unmark_best_answer_closed_thread(self):
        """
        api validates if user has permission to unmark best answer in closed thread
        """
        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl(
        {
            "can_mark_best_answers": 0,
            "can_change_marked_answers": 2,
            "can_protect_posts": 0,
        }
    )
    def test_unmark_best_answer_protected_no_permission(self):
        """api validates permission to unmark protected best answers"""
        self.thread.best_answer_is_protected = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.id,
                "detail": [
                    "You don't have permission to unmark this thread's best answer "
                    "because a moderator has protected it."
                ],
            },
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json["best_answer"], self.best_answer.id)

    @patch_category_acl(
        {
            "can_mark_best_answers": 0,
            "can_change_marked_answers": 2,
            "can_protect_posts": 1,
        }
    )
    def test_unmark_best_answer_protected(self):
        """api validates permission to unmark protected best answers"""
        self.thread.best_answer_is_protected = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "best-answer", "value": self.best_answer.id}],
        )
        self.assertEqual(response.status_code, 200)
