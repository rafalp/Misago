# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.utils.encoding import smart_str

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase

from .. import testutils
from ..models import Thread


class EditReplyTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(EditReplyTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.post = testutils.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse('misago:api:thread-post-detail', kwargs={
            'thread_pk': self.thread.pk,
            'pk': self.post.pk
        })

    def override_acl(self, extra_acl=None):
        new_acl = self.user.acl
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 0,
            'can_reply_threads': 0,
            'can_edit_posts': 1
        })

        if extra_acl:
            new_acl['categories'][self.category.pk].update(extra_acl)

        override_acl(self.user, new_acl)

    def put(self, url, data=None):
        content = encode_multipart(BOUNDARY, data or {})
        return self.client.put(url, content, content_type=MULTIPART_CONTENT)

    def test_cant_edit_reply_as_guest(self):
        """user has to be authenticated to be able to edit reply"""
        self.logout_user()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_thread_visibility(self):
        """thread's visibility is validated"""
        self.override_acl({'can_see': 0})
        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 404)

        self.override_acl({'can_browse': 0})
        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 404)

        self.override_acl({'can_see_all_threads': 0})
        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_cant_edit_reply(self):
        """permission to edit reply is validated"""
        self.override_acl({
            'can_edit_posts': 0
        })

        response = self.put(self.api_link)
        self.assertContains(response, "You can't edit posts in this category.", status_code=403)

    def test_cant_edit_other_user_reply(self):
        """permission to edit reply by other users is validated"""
        self.override_acl({
            'can_edit_posts': 1
        })

        self.post.poster = None
        self.post.save()

        response = self.put(self.api_link)
        self.assertContains(response, "You can't edit other users posts in this category.", status_code=403)

    def test_closed_category(self):
        """permssion to edit reply in closed category is validated"""
        self.override_acl({
            'can_close_threads': 0
        })

        self.category.is_closed = True
        self.category.save()

        response = self.put(self.api_link)
        self.assertContains(response, "This category is closed. You can't edit posts in it.", status_code=403)

        # allow to post in closed category
        self.override_acl({
            'can_close_threads': 1
        })

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_closed_thread(self):
        """permssion to edit reply in closed thread is validated"""
        self.override_acl({
            'can_close_threads': 0
        })

        self.thread.is_closed = True
        self.thread.save()

        response = self.put(self.api_link)
        self.assertContains(response, "This thread is closed. You can't edit posts in it.", status_code=403)

        # allow to post in closed thread
        self.override_acl({
            'can_close_threads': 1
        })

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_protected_post(self):
        """permssion to edit protected post is validated"""
        self.override_acl({
            'can_protect_posts': 0
        })

        self.post.is_protected = True
        self.post.save()

        response = self.put(self.api_link)
        self.assertContains(response, "This post is protected. You can't edit it.", status_code=403)

        # allow to post in closed thread
        self.override_acl({
            'can_protect_posts': 1
        })

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_empty_data(self):
        """no data sent handling has no showstoppers"""
        self.override_acl()

        response = self.put(self.api_link, data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(smart_str(response.content)), {
            'post': [
                "You have to enter a message."
            ]
        })

    def test_post_is_validated(self):
        """post is validated"""
        self.override_acl()

        response = self.put(self.api_link, data={
            'post': "a",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(smart_str(response.content)), {
            'post': [
                "Posted message should be at least 5 characters long (it has 1)."
            ]
        })

    def _test_can_reply_thread(self):
        """endpoint creates new reply"""
        self.override_acl()
        response = self.put(self.api_link, data={
            'post': "This is test response!"
        })
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(pk=self.thread.pk)

        self.override_acl()
        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, "<p>This is test response!</p>")

        self.reload_user()
        self.assertEqual(self.user.posts, 1)

        post = self.user.post_set.all()[:1][0]
        self.assertEqual(post.category_id, self.category.pk)
        self.assertEqual(post.original, "This is test response!")
        self.assertEqual(post.poster_id, self.user.id)
        self.assertEqual(post.poster_name, self.user.username)

        self.assertEqual(thread.last_post_id, post.id)
        self.assertEqual(thread.last_poster_id, self.user.id)
        self.assertEqual(thread.last_poster_name, self.user.username)
        self.assertEqual(thread.last_poster_slug, self.user.slug)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.last_thread_id, thread.id)
        self.assertEqual(category.last_thread_title, thread.title)
        self.assertEqual(category.last_thread_slug, thread.slug)

        self.assertEqual(category.last_poster_id, self.user.id)
        self.assertEqual(category.last_poster_name, self.user.username)
        self.assertEqual(category.last_poster_slug, self.user.slug)

    def test_protect_post(self):
        """can protect post"""
        self.override_acl({
            'can_protect_posts': 1
        })

        response = self.put(self.api_link, data={
            'post': "Lorem ipsum dolor met!",
            'protect': 1
        })
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.all()[:1][0]
        self.assertTrue(post.is_protected)

    def test_protect_post_no_permission(self):
        """cant protect post without permission"""
        self.override_acl({
            'can_protect_posts': 0
        })

        response = self.put(self.api_link, data={
            'post': "Lorem ipsum dolor met!",
            'protect': 1
        })
        self.assertEqual(response.status_code, 200)

        post = self.user.post_set.all()[:1][0]
        self.assertFalse(post.is_protected)

    def test_post_unicode(self):
        """unicode characters can be posted"""
        self.override_acl()

        response = self.put(self.api_link, data={
            'post': "Chrzążczyżewoszyce, powiat Łękółody."
        })
        self.assertEqual(response.status_code, 200)
