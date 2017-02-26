# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.models import Post
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadPostPatchApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadPostPatchApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.post = testutils.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            'misago:api:thread-post-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.post.pk,
            }
        )

    def patch(self, api_link, ops):
        return self.client.patch(api_link, json.dumps(ops), content_type="application/json")

    def refresh_post(self):
        self.post = self.thread.post_set.get(pk=self.post.pk)

    def override_acl(self, extra_acl=None):
        new_acl = self.user.acl_cache
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 0,
            'can_reply_threads': 0,
            'can_edit_posts': 1,
        })

        if extra_acl:
            new_acl['categories'][self.category.pk].update(extra_acl)

        override_acl(self.user, new_acl)


class PostAddAclApiTests(ThreadPostPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds current event's acl to response"""
        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': True,
            },
        ])
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertTrue(response_json['acl'])

    def test_add_acl_false(self):
        """if value is false, api won't add acl to the response, but will set empty key"""
        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': False,
            },
        ])
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIsNone(response_json['acl'])

        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': True,
            },
        ])
        self.assertEqual(response.status_code, 200)


class PostProtectApiTests(ThreadPostPatchApiTestCase):
    def test_protect_post(self):
        """api makes it possible to protect post"""
        self.override_acl({'can_protect_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-protected',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertTrue(self.post.is_protected)

    def test_unprotect_post(self):
        """api makes it possible to unprotect protected post"""
        self.post.is_protected = True
        self.post.save()

        self.override_acl({'can_protect_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-protected',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertFalse(self.post.is_protected)

    def test_protect_post_no_permission(self):
        """api validates permission to protect post"""
        self.override_acl({'can_protect_posts': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-protected',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't protect posts in this category.")

        self.refresh_post()
        self.assertFalse(self.post.is_protected)

    def test_unprotect_post_no_permission(self):
        """api validates permission to unprotect post"""
        self.post.is_protected = True
        self.post.save()

        self.override_acl({'can_protect_posts': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-protected',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't protect posts in this category.")

        self.refresh_post()
        self.assertTrue(self.post.is_protected)

    def test_unprotect_post_not_editable(self):
        """api validates if we can edit post we want to protect"""
        self.override_acl({'can_edit_posts': 0, 'can_protect_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-protected',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't protect posts you can't edit.")

        self.refresh_post()
        self.assertFalse(self.post.is_protected)


class PostApproveApiTests(ThreadPostPatchApiTestCase):
    def test_approve_post(self):
        """api makes it possible to approve post"""
        self.post.is_unapproved = True
        self.post.save()

        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-unapproved',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertFalse(self.post.is_unapproved)

    def test_unapprove_post(self):
        """unapproving posts is not supported by api"""
        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-unapproved',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertFalse(self.post.is_unapproved)

    def test_approve_post_no_permission(self):
        """api validates approval permission"""
        self.post.is_unapproved = True
        self.post.save()

        self.override_acl({'can_approve_content': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-unapproved',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't approve posts in this category.")

        self.refresh_post()
        self.assertTrue(self.post.is_unapproved)

    def test_approve_first_post(self):
        """api approve first post fails"""
        self.post.is_unapproved = True
        self.post.save()

        self.thread.set_first_post(self.post)
        self.thread.save()

        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-unapproved',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't approve thread's first post.")

        self.refresh_post()
        self.assertTrue(self.post.is_unapproved)

    def test_approve_hidden_post(self):
        """api approve hidden post fails"""
        self.post.is_unapproved = True
        self.post.is_hidden = True
        self.post.save()

        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-unapproved',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You can't approve posts the content you can't see."
        )

        self.refresh_post()
        self.assertTrue(self.post.is_unapproved)


class PostHideApiTests(ThreadPostPatchApiTestCase):
    def test_hide_post(self):
        """api makes it possible to hide post"""
        self.override_acl({'can_hide_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_show_post(self):
        """api makes it possible to unhide post"""
        self.post.is_hidden = True
        self.post.save()

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

        self.override_acl({'can_hide_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_hide_own_post(self):
        """api makes it possible to hide owned post"""
        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_show_own_post(self):
        """api makes it possible to unhide owned post"""
        self.post.is_hidden = True
        self.post.save()

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_hide_post_no_permission(self):
        """api hide post with no permission fails"""
        self.override_acl({'can_hide_posts': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't hide posts in this category.")

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_show_post_no_permission(self):
        """api unhide post with no permission fails"""
        self.post.is_hidden = True
        self.post.save()

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

        self.override_acl({'can_hide_posts': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't reveal posts in this category.")

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_hide_own_protected_post(self):
        """api validates if we are trying to hide protected post"""
        self.post.is_protected = True
        self.post.save()

        self.override_acl({'can_protect_posts': 0, 'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "This post is protected. You can't hide it.")

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_show_own_protected_post(self):
        """api validates if we are trying to reveal protected post"""
        self.post.is_hidden = True
        self.post.save()

        self.override_acl({'can_protect_posts': 0, 'can_hide_own_posts': 1})

        self.post.is_protected = True
        self.post.save()

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "This post is protected. You can't reveal it."
        )

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_hide_other_user_post(self):
        """api validates post ownership when hiding"""
        self.post.poster = None
        self.post.save()

        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You can't hide other users posts in this category."
        )

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_show_other_user_post(self):
        """api validates post ownership when revealing"""
        self.post.is_hidden = True
        self.post.poster = None
        self.post.save()

        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You can't reveal other users posts in this category."
        )

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_hide_own_post_after_edit_time(self):
        """api validates if we are trying to hide post after edit time"""
        self.post.posted_on = timezone.now() - timedelta(minutes=10)
        self.post.save()

        self.override_acl({'post_edit_time': 1, 'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You can't hide posts that are older than 1 minute."
        )

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_show_own_post_after_edit_time(self):
        """api validates if we are trying to reveal post after edit time"""
        self.post.is_hidden = True
        self.post.posted_on = timezone.now() - timedelta(minutes=10)
        self.post.save()

        self.override_acl({'post_edit_time': 1, 'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You can't reveal posts that are older than 1 minute."
        )

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_hide_post_in_closed_thread(self):
        """api validates if we are trying to hide post in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "This thread is closed. You can't hide posts in it."
        )

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_show_post_in_closed_thread(self):
        """api validates if we are trying to reveal post in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        self.post.is_hidden = True
        self.post.save()

        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "This thread is closed. You can't reveal posts in it."
        )

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_hide_post_in_closed_category(self):
        """api validates if we are trying to hide post in closed category"""
        self.category.is_closed = True
        self.category.save()

        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "This category is closed. You can't hide posts in it."
        )

        self.refresh_post()
        self.assertFalse(self.post.is_hidden)

    def test_show_post_in_closed_category(self):
        """api validates if we are trying to reveal post in closed category"""
        self.category.is_closed = True
        self.category.save()

        self.post.is_hidden = True
        self.post.save()

        self.override_acl({'can_hide_own_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "This category is closed. You can't reveal posts in it."
        )

        self.refresh_post()
        self.assertTrue(self.post.is_hidden)

    def test_hide_first_post(self):
        """api hide first post fails"""
        self.thread.set_first_post(self.post)
        self.thread.save()

        self.override_acl({'can_hide_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't hide thread's first post.")

    def test_show_first_post(self):
        """api unhide first post fails"""
        self.thread.set_first_post(self.post)
        self.thread.save()

        self.override_acl({'can_hide_posts': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't reveal thread's first post.")


class PostLikeApiTests(ThreadPostPatchApiTestCase):
    def test_like_no_see_permission(self):
        """api validates user's permission to see posts likes"""
        self.override_acl({'can_see_posts_likes': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-liked',
                    'value': True,
                },
            ]
        )
        self.assertContains(response, "You can't like posts in this category.", status_code=400)

    def test_like_no_like_permission(self):
        """api validates user's permission to see posts likes"""
        self.override_acl({'can_like_posts': False})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-liked',
                    'value': True,
                },
            ]
        )
        self.assertContains(response, "You can't like posts in this category.", status_code=400)

    def test_like_post(self):
        """api adds user like to post"""
        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-liked',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['likes'], 1)
        self.assertEqual(response_json['is_liked'], True)
        self.assertEqual(
            response_json['last_likes'], [
                {
                    'id': self.user.id,
                    'username': self.user.username,
                },
            ]
        )

        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.likes, response_json['likes'])
        self.assertEqual(post.last_likes, response_json['last_likes'])

    def test_like_liked_post(self):
        """api adds user like to post"""
        testutils.like_post(self.post, username='Myo')
        testutils.like_post(self.post, username='Mugi')
        testutils.like_post(self.post, username='Bob')
        testutils.like_post(self.post, username='Miku')

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-liked',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['likes'], 5)
        self.assertEqual(response_json['is_liked'], True)
        self.assertEqual(
            response_json['last_likes'], [
                {
                    'id': self.user.id,
                    'username': self.user.username
                },
                {
                    'id': None,
                    'username': 'Miku',
                },
                {
                    'id': None,
                    'username': 'Bob',
                },
                {
                    'id': None,
                    'username': 'Mugi',
                },
            ]
        )

        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.likes, response_json['likes'])
        self.assertEqual(post.last_likes, response_json['last_likes'])

    def test_unlike_post(self):
        """api removes user like from post"""
        testutils.like_post(self.post, self.user)

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-liked',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['likes'], 0)
        self.assertEqual(response_json['is_liked'], False)
        self.assertEqual(response_json['last_likes'], [])

        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.likes, response_json['likes'])
        self.assertEqual(post.last_likes, response_json['last_likes'])

    def test_like_post_no_change(self):
        """api does no state change if we are linking liked post"""
        testutils.like_post(self.post, self.user)

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-liked',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['likes'], 1)
        self.assertEqual(response_json['is_liked'], True)
        self.assertEqual(
            response_json['last_likes'], [
                {
                    'id': self.user.id,
                    'username': self.user.username,
                },
            ]
        )

        post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(post.likes, response_json['likes'])
        self.assertEqual(post.last_likes, response_json['last_likes'])

    def test_unlike_post_no_change(self):
        """api does no state change if we are unlinking unliked post"""
        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-liked',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['likes'], 0)
        self.assertEqual(response_json['is_liked'], False)
        self.assertEqual(response_json['last_likes'], [])


class ThreadEventPatchApiTestCase(ThreadPostPatchApiTestCase):
    def setUp(self):
        super(ThreadEventPatchApiTestCase, self).setUp()

        self.event = testutils.reply_thread(self.thread, poster=self.user, is_event=True)

        self.api_link = reverse(
            'misago:api:thread-post-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.event.pk,
            }
        )

    def refresh_event(self):
        self.event = self.thread.post_set.get(pk=self.event.pk)


class EventAnonPatchApiTests(ThreadEventPatchApiTestCase):
    def test_anonymous_user(self):
        """anonymous users can't change event state"""
        self.logout_user()

        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': True,
            },
        ])
        self.assertEqual(response.status_code, 403)


class EventAddAclApiTests(ThreadEventPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds current event's acl to response"""
        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': True,
            },
        ])
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertTrue(response_json['acl'])

    def test_add_acl_false(self):
        """if value is false, api won't add acl to the response, but will set empty key"""
        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': False,
            },
        ])
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIsNone(response_json['acl'])

        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': True,
            },
        ])
        self.assertEqual(response.status_code, 200)


class EventHideApiTests(ThreadEventPatchApiTestCase):
    def test_hide_event(self):
        """api makes it possible to hide event"""
        self.override_acl({'can_hide_events': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_event()
        self.assertTrue(self.event.is_hidden)

    def test_show_event(self):
        """api makes it possible to unhide event"""
        self.event.is_hidden = True
        self.event.save()

        self.refresh_event()
        self.assertTrue(self.event.is_hidden)

        self.override_acl({'can_hide_events': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.refresh_event()
        self.assertFalse(self.event.is_hidden)

    def test_hide_event_no_permission(self):
        """api hide event with no permission fails"""
        self.override_acl({'can_hide_events': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to hide this event."
        )

        self.refresh_event()
        self.assertFalse(self.event.is_hidden)

    def test_show_event_no_permission(self):
        """api unhide event with no permission fails"""
        self.event.is_hidden = True
        self.event.save()

        self.refresh_event()
        self.assertTrue(self.event.is_hidden)

        self.override_acl({'can_hide_events': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 404)
