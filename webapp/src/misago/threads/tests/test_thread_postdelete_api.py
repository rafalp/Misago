from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from .. import test
from ..models import Post, Thread
from ..test import patch_category_acl
from .test_threads_api import ThreadsApiTestCase


class PostDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.post = test.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.post.pk},
        )

    def test_delete_anonymous(self):
        """api validates if deleting user is authenticated"""
        self.logout_user()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    @patch_category_acl({"can_hide_posts": 1, "can_hide_own_posts": 1})
    def test_no_permission(self):
        """api validates permission to delete post"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete posts in this category."}
        )

    @patch_category_acl(
        {"can_hide_posts": 1, "can_hide_own_posts": 2, "post_edit_time": 0}
    )
    def test_delete_other_user_post_no_permission(self):
        """api valdiates if user can delete other users posts"""
        self.post.poster = None
        self.post.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete other users posts in this category."},
        )

    @patch_category_acl(
        {"can_hide_posts": 1, "can_hide_own_posts": 2, "post_edit_time": 0}
    )
    def test_delete_protected_post_no_permission(self):
        """api validates if user can delete protected post"""
        self.post.is_protected = True
        self.post.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This post is protected. You can't delete it."}
        )

    @patch_category_acl(
        {"can_hide_posts": 1, "can_hide_own_posts": 2, "post_edit_time": 1}
    )
    def test_delete_protected_post_after_edit_time(self):
        """api validates if user can delete delete post after edit time"""
        self.post.posted_on = timezone.now() - timedelta(minutes=10)
        self.post.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete posts that are older than 1 minute."},
        )

    @patch_category_acl(
        {
            "can_hide_posts": 0,
            "can_hide_own_posts": 2,
            "post_edit_time": 0,
            "can_close_threads": False,
        }
    )
    def test_delete_post_closed_thread_no_permission(self):
        """api valdiates if user can delete posts in closed threads"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't delete posts in it."},
        )

    @patch_category_acl(
        {
            "can_hide_posts": 0,
            "can_hide_own_posts": 2,
            "post_edit_time": 0,
            "can_close_threads": False,
        }
    )
    def test_delete_post_closed_category_no_permission(self):
        """api valdiates if user can delete posts in closed categories"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't delete posts in it."},
        )

    @patch_category_acl({"can_hide_posts": 2, "can_hide_own_posts": 2})
    def test_delete_first_post(self):
        """api disallows first post deletion"""
        api_link = reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.thread.first_post_id},
        )

        response = self.client.delete(api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete thread's first post."}
        )

    @patch_category_acl({"can_hide_posts": 2, "can_hide_own_posts": 2})
    def test_delete_best_answer(self):
        """api disallows best answer deletion"""
        self.thread.set_best_answer(self.user, self.post)
        self.thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete this post because its marked as best answer."},
        )

    @patch_category_acl(
        {"can_hide_posts": 0, "can_hide_own_posts": 2, "post_edit_time": 0}
    )
    def test_delete_owned_post(self):
        """api deletes owned thread post"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, self.post.pk)
        with self.assertRaises(Post.DoesNotExist):
            self.thread.post_set.get(pk=self.post.pk)

    @patch_category_acl({"can_hide_posts": 2, "can_hide_own_posts": 0})
    def test_delete_post(self):
        """api deletes thread post"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, self.post.pk)
        with self.assertRaises(Post.DoesNotExist):
            self.thread.post_set.get(pk=self.post.pk)


class EventDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.event = test.reply_thread(self.thread, poster=self.user, is_event=True)

        self.api_link = reverse(
            "misago:api:thread-post-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.event.pk},
        )

    def test_delete_anonymous(self):
        """api validates if deleting user is authenticated"""
        self.logout_user()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    @patch_category_acl(
        {"can_hide_posts": 2, "can_hide_own_posts": 0, "can_hide_events": 0}
    )
    def test_no_permission(self):
        """api validates permission to delete event"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete events in this category."}
        )

    @patch_category_acl(
        {
            "can_hide_posts": 2,
            "can_hide_own_posts": 0,
            "can_hide_events": 2,
            "can_close_threads": False,
        }
    )
    def test_delete_event_closed_thread_no_permission(self):
        """api valdiates if user can delete events in closed threads"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't delete events in it."},
        )

    @patch_category_acl(
        {"can_hide_posts": 2, "can_hide_events": 2, "can_close_threads": False}
    )
    def test_delete_event_closed_category_no_permission(self):
        """api valdiates if user can delete events in closed categories"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't delete events in it."},
        )

    @patch_category_acl({"can_hide_posts": 0, "can_hide_events": 2})
    def test_delete_event(self):
        """api differs posts from events"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, self.event.pk)
        with self.assertRaises(Post.DoesNotExist):
            self.thread.post_set.get(pk=self.event.pk)
