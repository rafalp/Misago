import json
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from misago.threads import testutils
from misago.threads.models import Post, Thread

from .test_threads_api import ThreadsApiTestCase


class PostBulkDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(PostBulkDeleteApiTests, self).setUp()

        self.posts = [
            testutils.reply_thread(self.thread, poster=self.user),
            testutils.reply_thread(self.thread),
            testutils.reply_thread(self.thread, poster=self.user),
        ]

        self.api_link = reverse(
            'misago:api:thread-post-list',
            kwargs={
                'thread_pk': self.thread.pk,
            }
        )

    def delete(self, url, data=None):
        return self.client.delete(url, json.dumps(data), content_type="application/json")

    def test_delete_anonymous(self):
        """api validates if deleting user is authenticated"""
        self.logout_user()

        response = self.delete(self.api_link)
        self.assertContains(response, "This action is not available to guests.", status_code=403)

    def test_delete_no_data(self):
        """api handles empty data"""
        response = self.client.delete(self.api_link, content_type="application/json")
        self.assertContains(response, "Expected a list of items", status_code=400)

    def test_delete_no_ids(self):
        """api requires ids to delete"""
        response = self.delete(self.api_link)
        self.assertContains(response, "You have to specify at least one post to delete.", status_code=400)

    def test_delete_empty_ids(self):
        """api requires ids to delete"""
        response = self.delete(self.api_link, [])
        self.assertContains(response, "You have to specify at least one post to delete.", status_code=400)

    def test_validate_ids(self):
        """api validates that ids are list of ints"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 2,
        })

        response = self.delete(self.api_link, True)
        self.assertContains(response, "Expected a list of items", status_code=400)

        response = self.delete(self.api_link, 'abbss')
        self.assertContains(response, "Expected a list of items", status_code=400)

        response = self.delete(self.api_link, [1, 2, 3, 'a', 'b', 'x'])
        self.assertContains(response, "One or more post ids received were invalid.", status_code=400)

    def test_validate_ids_length(self):
        """api validates that ids are list of ints"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 2,
        })

        response = self.delete(self.api_link, list(range(100)))
        self.assertContains(response, "No more than 24 posts can be deleted at single time.", status_code=400)

    def test_validate_posts_exist(self):
        """api validates that ids are visible posts"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        response = self.delete(self.api_link, [p.id * 10 for p in self.posts])
        self.assertContains(response, "One or more posts to delete could not be found.", status_code=403)

    def test_validate_posts_visibility(self):
        """api validates that ids are visible posts"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        self.posts[1].is_unapproved = True
        self.posts[1].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(response, "One or more posts to delete could not be found.", status_code=403)

    def test_validate_posts_same_thread(self):
        """api validates that ids are visible posts"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 2,
        })

        other_thread = testutils.post_thread(category=self.category)
        self.posts.append(testutils.reply_thread(other_thread, poster=self.user))

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(response, "One or more posts to delete could not be found.", status_code=403)

    def test_no_permission(self):
        """api validates permission to delete"""
        self.override_acl({
            'can_hide_own_posts': 1,
            'can_hide_posts': 1,
        })

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(response, "You can't delete posts in this category.", status_code=403)

    def test_delete_other_user_post_no_permission(self):
        """api valdiates if user can delete other users posts"""
        self.override_acl({
            'post_edit_time': 0,
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(
            response, "You can't delete other users posts in this category", status_code=403
        )

    def test_delete_protected_post_no_permission(self):
        """api validates if user can delete protected post"""
        self.override_acl({
            'can_protect_posts': 0,
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        self.posts[0].is_protected = True
        self.posts[0].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(
            response, "This post is protected. You can't delete it.", status_code=403
        )

    def test_delete_protected_post_after_edit_time(self):
        """api validates if user can delete delete post after edit time"""
        self.override_acl({
            'post_edit_time': 1,
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        self.posts[0].posted_on = timezone.now() - timedelta(minutes=10)
        self.posts[0].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(
            response, "You can't delete posts that are older than 1 minute.", status_code=403
        )

    def test_delete_post_closed_thread_no_permission(self):
        """api valdiates if user can delete posts in closed threads"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        self.thread.is_closed = True
        self.thread.save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(
            response, "This thread is closed. You can't delete posts in it.", status_code=403
        )

    def test_delete_post_closed_category_no_permission(self):
        """api valdiates if user can delete posts in closed categories"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        self.category.is_closed = True
        self.category.save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(
            response, "This category is closed. You can't delete posts in it.", status_code=403
        )

    def test_delete_first_post(self):
        """api disallows first post's deletion"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 2,
        })

        ids = [p.id for p in self.posts]
        ids.append(self.thread.first_post_id)

        response = self.delete(self.api_link, ids)
        self.assertContains(response, "You can't delete thread's first post.", status_code=403)

    def test_delete_event(self):
        """api differs posts from events"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 2,
            'can_hide_events': 0,
        })

        self.posts[1].is_event = True
        self.posts[1].save()

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertContains(response, "You can't delete events in this category.", status_code=403)

    def test_delete_owned_posts(self):
        """api deletes owned thread posts"""
        self.override_acl({
            'post_edit_time': 0,
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        ids = [self.posts[0].id, self.posts[-1].id]

        response = self.delete(self.api_link, ids)
        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, ids[-1])
        for post in ids:
            with self.assertRaises(Post.DoesNotExist):
                self.thread.post_set.get(pk=post)

    def test_delete_posts(self):
        """api deletes thread posts"""
        self.override_acl({
            'can_hide_own_posts': 0,
            'can_hide_posts': 2,
        })

        response = self.delete(self.api_link, [p.id for p in self.posts])
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, self.posts[-1].pk)
        for post in self.posts:
            with self.assertRaises(Post.DoesNotExist):
                self.thread.post_set.get(pk=post.pk)
