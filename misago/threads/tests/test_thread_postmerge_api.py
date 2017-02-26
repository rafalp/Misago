# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.api.postendpoints.merge import MERGE_LIMIT
from misago.threads.models import Post, Thread
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadPostMergeApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadPostMergeApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.post = testutils.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            'misago:api:thread-post-merge', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

        self.override_acl()

    def refresh_thread(self):
        self.thread = Thread.objects.get(pk=self.thread.pk)

    def override_acl(self, extra_acl=None):
        new_acl = self.user.acl_cache
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 0,
            'can_reply_threads': 0,
            'can_edit_posts': 1,
            'can_approve_content': 0,
            'can_merge_posts': 1,
        })

        if extra_acl:
            new_acl['categories'][self.category.pk].update(extra_acl)

        override_acl(self.user, new_acl)

    def test_anonymous_user(self):
        """you need to authenticate to merge posts"""
        self.logout_user()

        response = self.client.post(
            self.api_link,
            json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_no_permission(self):
        """api validates permission to merge"""
        self.override_acl({'can_merge_posts': 0})

        response = self.client.post(
            self.api_link,
            json.dumps({}),
            content_type="application/json",
        )
        self.assertContains(response, "You can't merge posts in this thread.", status_code=403)

    def test_closed_thread(self):
        """api validates permission to merge in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps({}),
            content_type="application/json",
        )
        self.assertContains(response, "You can't merge posts in this thread.", status_code=403)

        # allow closing threads
        self.override_acl({'can_close_threads': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({}),
            content_type="application/json",
        )
        self.assertContains(
            response, "You have to select at least two posts to merge.", status_code=400
        )

    def test_closed_category(self):
        """api validates permission to merge in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            json.dumps({}),
            content_type="application/json",
        )
        self.assertContains(response, "You can't merge posts in this thread.", status_code=403)

        # allow closing threads
        self.override_acl({'can_close_threads': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({}),
            content_type="application/json",
        )
        self.assertContains(
            response, "You have to select at least two posts to merge.", status_code=400
        )

    def test_empty_data(self):
        """api handles empty data"""
        response = self.client.post(
            self.api_link,
            json.dumps({}),
            content_type="application/json",
        )
        self.assertContains(
            response, "You have to select at least two posts to merge.", status_code=400
        )

    def test_no_posts_ids(self):
        """api rejects no posts ids"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': []
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "You have to select at least two posts to merge.", status_code=400
        )

    def test_invalid_posts_data(self):
        """api handles invalid data"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': 'string'
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more post ids received were invalid.", status_code=400
        )

    def test_invalid_posts_ids(self):
        """api handles invalid post id"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [1, 2, 'string']
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more post ids received were invalid.", status_code=400
        )

    def test_one_post_id(self):
        """api rejects one post id"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [1]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "You have to select at least two posts to merge.", status_code=400
        )

    def test_merge_limit(self):
        """api rejects more posts than merge limit"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': list(range(MERGE_LIMIT + 1))
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "No more than {} posts can be merged".format(MERGE_LIMIT), status_code=400
        )

    def test_merge_event(self):
        """api recjects events"""
        event = testutils.reply_thread(self.thread, is_event=True, poster=self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [self.post.pk, event.pk]
            }),
            content_type="application/json",
        )
        self.assertContains(response, "Events can't be merged.", status_code=400)

    def test_merge_notfound_pk(self):
        """api recjects nonexistant pk's"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [self.post.pk, self.post.pk * 1000]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more posts to merge could not be found.", status_code=400
        )

    def test_merge_cross_threads(self):
        """api recjects attempt to merge with post made in other thread"""
        other_thread = testutils.post_thread(category=self.category)
        other_post = testutils.reply_thread(other_thread, poster=self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [self.post.pk, other_post.pk]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more posts to merge could not be found.", status_code=400
        )

    def test_merge_authenticated_with_guest_post(self):
        """api recjects attempt to merge with post made by deleted user"""
        other_post = testutils.reply_thread(self.thread)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [self.post.pk, other_post.pk]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "Posts made by different users can't be merged.", status_code=400
        )

    def test_merge_guest_with_authenticated_post(self):
        """api recjects attempt to merge with post made by deleted user"""
        other_post = testutils.reply_thread(self.thread)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [other_post.pk, self.post.pk]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "Posts made by different users can't be merged.", status_code=400
        )

    def test_merge_guest_posts_different_usernames(self):
        """api recjects attempt to merge posts made by different guests"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [
                    testutils.reply_thread(self.thread, poster="Bob").pk,
                    testutils.reply_thread(self.thread, poster="Miku").pk,
                ]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "Posts made by different users can't be merged.", status_code=400
        )

    def test_merge_different_visibility(self):
        """api recjects attempt to merge posts with different visibility"""
        self.override_acl({'can_hide_posts': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [
                    testutils.reply_thread(self.thread, poster="Bob", is_hidden=True).pk,
                    testutils.reply_thread(self.thread, poster="Bob", is_hidden=False).pk,
                ]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "Posts with different visibility can't be merged.", status_code=400
        )

    def test_merge_different_approval(self):
        """api recjects attempt to merge posts with different approval"""
        self.override_acl({'can_approve_content': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [
                    testutils.reply_thread(self.thread, poster="Bob", is_unapproved=True).pk,
                    testutils.reply_thread(self.thread, poster="Bob", is_unapproved=False).pk,
                ]
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "Posts with different visibility can't be merged.", status_code=400
        )

    def test_merge_posts(self):
        """api merges two posts"""
        post_a = testutils.reply_thread(self.thread, poster=self.user, message="Battęry")
        post_b = testutils.reply_thread(self.thread, poster=self.user, message="Hórse")

        thread_replies = self.thread.replies

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [post_a.pk, post_b.pk]
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_thread()
        self.assertEqual(self.thread.replies, thread_replies - 1)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=post_b.pk)

        merged_post = Post.objects.get(pk=post_a.pk)
        self.assertEqual(merged_post.parsed, '{}\n{}'.format(post_a.parsed, post_b.parsed))

    def test_merge_hidden_posts(self):
        """api merges two hidden posts"""
        self.override_acl({'can_hide_posts': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [
                    testutils.reply_thread(self.thread, poster=self.user, is_hidden=True).pk,
                    testutils.reply_thread(self.thread, poster=self.user, is_hidden=True).pk,
                ]
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_merge_unapproved_posts(self):
        """api merges two unapproved posts"""
        self.override_acl({'can_approve_content': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [
                    testutils.reply_thread(self.thread, poster=self.user, is_unapproved=True).pk,
                    testutils.reply_thread(self.thread, poster=self.user, is_unapproved=True).pk,
                ]
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_merge_with_hidden_thread(self):
        """api recjects attempt to merge posts with different visibility"""
        self.thread.first_post.is_hidden = True
        self.thread.first_post.poster = self.user
        self.thread.first_post.save()

        post_visible = testutils.reply_thread(self.thread, poster=self.user, is_hidden=False)

        self.override_acl({'can_hide_threads': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [self.thread.first_post.pk, post_visible.pk]
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
