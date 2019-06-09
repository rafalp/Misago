import json
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from .. import test
from ..models import Post, Thread
from ..test import patch_category_acl
from .test_threads_api import ThreadsApiTestCase


class PostBulkDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.posts = [
            test.reply_thread(self.thread, poster=self.user),
            test.reply_thread(self.thread),
            test.reply_thread(self.thread, poster=self.user),
        ]

        self.api_link = reverse(
            "misago:api:thread-post-list", kwargs={"thread_pk": self.thread.pk}
        )

    def delete(self, url, data=None):
        return self.client.delete(
            url, json.dumps(data), content_type="application/json"
        )

    def test_delete_anonymous(self):
        """api validates if deleting user is authenticated"""
        self.logout_user()

        response = self.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    def test_delete_no_data(self):
        """api handles empty data"""
        response = self.client.delete(self.api_link, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "dict".'}
        )

    def test_delete_no_ids(self):
        """api requires ids to delete"""
        response = self.delete(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to delete."},
        )

    def test_delete_empty_ids(self):
        """api requires ids to delete"""
        response = self.delete(self.api_link, [])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to delete."},
        )

    @patch_category_acl({"can_hide_posts": 2})
    def test_validate_ids(self):
        """api validates that ids are list of ints"""
        response = self.delete(self.api_link, True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "bool".'}
        )

        response = self.delete(self.api_link, "abbss")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "str".'}
        )

        response = self.delete(self.api_link, [1, 2, 3, "a", "b", "x"])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "One or more post ids received were invalid."}
        )

    @patch_category_acl({"can_hide_posts": 2})
    def test_validate_ids_length(self):
        """api validates that ids are list of ints"""
        response = self.delete(self.api_link, list(range(100)))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "No more than 24 posts can be deleted at a single time."},
        )

    @patch_category_acl({"can_hide_posts": 2})
    def test_validate_posts_exist(self):
        """api validates that ids are visible posts"""
        response = self.delete(self.api_link, [p.id * 10 for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to delete could not be found."},
        )

    @patch_category_acl({"can_hide_posts": 2})
    def test_validate_posts_visibility(self):
        """api validates that ids are visible posts"""
        self.posts[1].is_unapproved = True
        self.posts[1].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to delete could not be found."},
        )

    @patch_category_acl({"can_hide_posts": 2})
    def test_validate_posts_same_thread(self):
        """api validates that ids are same thread posts"""
        other_thread = test.post_thread(category=self.category)
        self.posts.append(test.reply_thread(other_thread, poster=self.user))

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to delete could not be found."},
        )

    @patch_category_acl({"can_hide_posts": 1, "can_hide_own_posts": 1})
    def test_no_permission(self):
        """api validates permission to delete"""
        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete posts in this category."}
        )

    @patch_category_acl(
        {"can_hide_posts": 0, "can_hide_own_posts": 2, "post_edit_time": 10}
    )
    def test_delete_other_user_post_no_permission(self):
        """api valdiates if user can delete other users posts"""
        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete other users posts in this category."},
        )

    @patch_category_acl(
        {"can_hide_posts": 0, "can_hide_own_posts": 2, "can_protect_posts": False}
    )
    def test_delete_protected_post_no_permission(self):
        """api validates if user can delete protected post"""
        self.posts[0].is_protected = True
        self.posts[0].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This post is protected. You can't delete it."}
        )

    @patch_category_acl(
        {"can_hide_posts": 0, "can_hide_own_posts": 2, "post_edit_time": 1}
    )
    def test_delete_protected_post_after_edit_time(self):
        """api validates if user can delete delete post after edit time"""
        self.posts[0].posted_on = timezone.now() - timedelta(minutes=10)
        self.posts[0].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete posts that are older than 1 minute."},
        )

    @patch_category_acl(
        {"can_hide_posts": 2, "can_hide_own_posts": 2, "can_close_threads": False}
    )
    def test_delete_post_closed_thread_no_permission(self):
        """api valdiates if user can delete posts in closed threads"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't delete posts in it."},
        )

    @patch_category_acl(
        {"can_hide_posts": 2, "can_hide_own_posts": 2, "can_close_threads": False}
    )
    def test_delete_post_closed_category_no_permission(self):
        """api valdiates if user can delete posts in closed categories"""
        self.category.is_closed = True
        self.category.save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't delete posts in it."},
        )

    @patch_category_acl({"can_hide_posts": 2, "can_hide_own_posts": 2})
    def test_delete_first_post(self):
        """api disallows first post's deletion"""
        ids = [p.id for p in self.posts]
        ids.append(self.thread.first_post_id)

        response = self.delete(self.api_link, ids)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete thread's first post."}
        )

    @patch_category_acl({"can_hide_posts": 2, "can_hide_own_posts": 2})
    def test_delete_best_answer(self):
        """api disallows best answer deletion"""
        self.thread.set_best_answer(self.user, self.posts[0])
        self.thread.save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't delete this post because its marked as best answer."},
        )

    @patch_category_acl(
        {"can_hide_posts": 2, "can_hide_own_posts": 2, "can_hide_events": 0}
    )
    def test_delete_event(self):
        """api differs posts from events"""
        self.posts[1].is_event = True
        self.posts[1].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't delete events in this category."}
        )

    @patch_category_acl(
        {"can_hide_posts": 0, "can_hide_own_posts": 2, "post_edit_time": 10}
    )
    def test_delete_owned_posts(self):
        """api deletes owned thread posts"""
        ids = [self.posts[0].id, self.posts[-1].id]

        response = self.delete(self.api_link, ids)
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)
        self.assertNotEqual(self.thread.last_post_id, ids[-1])

        for post in ids:
            with self.assertRaises(Post.DoesNotExist):
                self.thread.post_set.get(pk=post)

    @patch_category_acl({"can_hide_posts": 2, "can_hide_own_posts": 0})
    def test_delete_posts(self):
        """api deletes thread posts"""
        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)
        self.assertNotEqual(self.thread.last_post_id, self.posts[-1].pk)

        for post in self.posts:
            with self.assertRaises(Post.DoesNotExist):
                self.thread.post_set.get(pk=post.pk)
