from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from misago.threads import testutils
from misago.threads.models import Post, Thread

from .test_threads_api import ThreadsApiTestCase


class PostDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(PostDeleteApiTests, self).setUp()

        self.post = testutils.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            'misago:api:thread-post-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.post.pk,
            }
        )

    def test_delete_anonymous(self):
        """api validates if deleting user is authenticated"""
        self.logout_user()

        response = self.client.delete(self.api_link)
        self.assertContains(response, "This action is not available to guests.", status_code=403)

    def test_no_permission(self):
        """api validates permission to delete post"""
        self.override_acl({'can_hide_own_posts': 1, 'can_hide_posts': 1})

        response = self.client.delete(self.api_link)
        self.assertContains(response, "You can't delete posts in this category.", status_code=403)

    def test_delete_other_user_post_no_permission(self):
        """api valdiates if user can delete other users posts"""
        self.override_acl({
            'post_edit_time': 0,
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        self.post.poster = None
        self.post.save()

        response = self.client.delete(self.api_link)
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

        self.post.is_protected = True
        self.post.save()

        response = self.client.delete(self.api_link)
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

        self.post.posted_on = timezone.now() - timedelta(minutes=10)
        self.post.save()

        response = self.client.delete(self.api_link)
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
        self.post.save()

        response = self.client.delete(self.api_link)
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
        self.post.save()

        response = self.client.delete(self.api_link)
        self.assertContains(
            response, "This category is closed. You can't delete posts in it.", status_code=403
        )

    def test_delete_first_post(self):
        """api disallows first post's deletion"""
        self.override_acl({'can_hide_own_posts': 2, 'can_hide_posts': 2})

        api_link = reverse(
            'misago:api:thread-post-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.thread.first_post_id,
            }
        )

        response = self.client.delete(api_link)
        self.assertContains(response, "You can't delete thread's first post.", status_code=403)

    def test_delete_event(self):
        """api differs posts from events"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 2,
            'can_hide_events': 0,
        })

        self.post.is_event = True
        self.post.save()

        response = self.client.delete(self.api_link)
        self.assertContains(response, "You can't delete events in this category.", status_code=403)

    def test_delete_owned_post(self):
        """api deletes owned thread post"""
        self.override_acl({
            'post_edit_time': 0,
            'can_hide_own_posts': 2,
            'can_hide_posts': 0,
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, self.post.pk)
        with self.assertRaises(Post.DoesNotExist):
            self.thread.post_set.get(pk=self.post.pk)

    def test_delete_post(self):
        """api deletes thread post"""
        self.override_acl({'can_hide_own_posts': 0, 'can_hide_posts': 2})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, self.post.pk)
        with self.assertRaises(Post.DoesNotExist):
            self.thread.post_set.get(pk=self.post.pk)


class EventDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(EventDeleteApiTests, self).setUp()

        self.event = testutils.reply_thread(self.thread, poster=self.user, is_event=True)

        self.api_link = reverse(
            'misago:api:thread-post-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.event.pk,
            }
        )

    def test_delete_anonymous(self):
        """api validates if deleting user is authenticated"""
        self.logout_user()

        response = self.client.delete(self.api_link)
        self.assertContains(response, "This action is not available to guests.", status_code=403)

    def test_no_permission(self):
        """api validates permission to delete event"""
        self.override_acl({
            'can_hide_own_posts': 2,
            'can_hide_posts': 2,
            'can_hide_events': 0,
        })

        response = self.client.delete(self.api_link)
        self.assertContains(response, "You can't delete events in this category.", status_code=403)

    def test_delete_event(self):
        """api differs posts from events"""
        self.override_acl({
            'can_hide_own_posts': 0,
            'can_hide_posts': 0,
            'can_hide_events': 2,
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.thread = Thread.objects.get(pk=self.thread.pk)

        self.assertNotEqual(self.thread.last_post_id, self.event.pk)
        with self.assertRaises(Post.DoesNotExist):
            self.thread.post_set.get(pk=self.event.pk)
