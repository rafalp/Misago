# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.api.postendpoints.move import MOVE_LIMIT
from misago.threads.models import Thread
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadPostMoveApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadPostMoveApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)

        self.api_link = reverse(
            'misago:api:thread-post-move', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

        Category(
            name='Category B',
            slug='category-b',
        ).insert_at(
            self.category,
            position='last-child',
            save=True,
        )
        self.category_b = Category.objects.get(slug='category-b')

        self.override_acl()
        self.override_other_acl()

    def refresh_thread(self):
        self.thread = Thread.objects.get(pk=self.thread.pk)

    def override_acl(self, extra_acl=None):
        new_acl = self.user.acl_cache
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 1,
            'can_reply_threads': 1,
            'can_edit_posts': 1,
            'can_approve_content': 0,
            'can_move_posts': 1,
        })

        if extra_acl:
            new_acl['categories'][self.category.pk].update(extra_acl)

        override_acl(self.user, new_acl)

    def override_other_acl(self, acl=None):
        other_category_acl = self.user.acl_cache['categories'][self.category.pk].copy()
        other_category_acl.update({
            'can_see': 1,
            'can_browse': 1,
            'can_start_threads': 0,
            'can_reply_threads': 0,
            'can_edit_posts': 1,
            'can_approve_content': 0,
            'can_move_posts': 1,
        })

        if acl:
            other_category_acl.update(acl)

        categories_acl = self.user.acl_cache['categories']
        categories_acl[self.category_b.pk] = other_category_acl

        visible_categories = [self.category.pk]
        if other_category_acl['can_see']:
            visible_categories.append(self.category_b.pk)

        override_acl(
            self.user, {
                'visible_categories': visible_categories,
                'categories': categories_acl,
            }
        )

    def test_anonymous_user(self):
        """you need to authenticate to move posts"""
        self.logout_user()

        response = self.client.post(self.api_link, json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_no_permission(self):
        """api validates permission to move"""
        self.override_acl({'can_move_posts': 0})

        response = self.client.post(self.api_link, json.dumps({}), content_type="application/json")
        self.assertContains(response, "You can't move posts in this thread.", status_code=403)

    def test_move_no_url(self):
        """api validates if thread url was given"""
        response = self.client.post(self.api_link)
        self.assertContains(response, "This is not a valid thread link.", status_code=400)

    def test_invalid_url(self):
        """api validates thread url"""
        response = self.client.post(self.api_link, {
            'thread_url': self.user.get_absolute_url(),
        })
        self.assertContains(response, "This is not a valid thread link.", status_code=400)

    def test_current_thread_url(self):
        """api validates if thread url given is to current thread"""
        response = self.client.post(
            self.api_link, {
                'thread_url': self.thread.get_absolute_url(),
            }
        )
        self.assertContains(
            response, "Thread to move posts to is same as current one.", status_code=400
        )

    def test_other_thread_exists(self):
        """api validates if other thread exists"""
        self.override_other_acl()

        other_thread = testutils.post_thread(self.category_b)
        other_thread_url = other_thread.get_absolute_url()
        other_thread.delete()

        response = self.client.post(self.api_link, {
            'thread_url': other_thread_url,
        })
        self.assertContains(
            response, "The thread you have entered link to doesn't exist", status_code=400
        )

    def test_other_thread_is_invisible(self):
        """api validates if other thread is visible"""
        self.override_other_acl({'can_see': 0})

        other_thread = testutils.post_thread(self.category_b)

        response = self.client.post(
            self.api_link, {
                'thread_url': other_thread.get_absolute_url(),
            }
        )
        self.assertContains(
            response, "The thread you have entered link to doesn't exist", status_code=400
        )

    def test_other_thread_isnt_replyable(self):
        """api validates if other thread can be replied"""
        self.override_other_acl({'can_reply_threads': 0})

        other_thread = testutils.post_thread(self.category_b)

        response = self.client.post(
            self.api_link, {
                'thread_url': other_thread.get_absolute_url(),
            }
        )
        self.assertContains(
            response, "You can't move posts to threads you can't reply.", status_code=400
        )

    def test_empty_data(self):
        """api handles empty data"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link, {
                'thread_url': other_thread.get_absolute_url(),
            }
        )
        self.assertContains(
            response, "You have to specify at least one post to move.", status_code=400
        )

    def test_no_posts_ids(self):
        """api rejects no posts ids"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': [],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "You have to specify at least one post to move.", status_code=400
        )

    def test_invalid_posts_data(self):
        """api handles invalid data"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': 'string',
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more post ids received were invalid.", status_code=400
        )

    def test_invalid_posts_ids(self):
        """api handles invalid post id"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': [1, 2, 'string'],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more post ids received were invalid.", status_code=400
        )

    def test_move_limit(self):
        """api rejects more posts than move limit"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': list(range(MOVE_LIMIT + 1)),
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "No more than {} posts can be moved".format(MOVE_LIMIT), status_code=400
        )

    def test_move_invisible(self):
        """api validates posts visibility"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread, is_unapproved=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more posts to move could not be found.", status_code=400
        )

    def test_move_other_thread_posts(self):
        """api recjects attempt to move other thread's post"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(other_thread, is_hidden=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more posts to move could not be found.", status_code=400
        )

    def test_move_event(self):
        """api rejects events move"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread, is_event=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(response, "Events can't be moved.", status_code=400)

    def test_move_first_post(self):
        """api rejects first post move"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': [self.thread.first_post_id],
            }),
            content_type="application/json",
        )
        self.assertContains(response, "You can't move thread's first post.", status_code=400)

    def test_move_hidden_posts(self):
        """api recjects attempt to move urneadable hidden post"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread, is_hidden=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "You can't move posts the content you can't see.", status_code=400
        )

    def test_move_posts(self):
        """api moves posts to other thread"""
        self.override_other_acl({'can_reply_threads': 1})

        other_thread = testutils.post_thread(self.category_b)

        posts = (
            testutils.reply_thread(self.thread).pk, testutils.reply_thread(self.thread).pk,
            testutils.reply_thread(self.thread).pk, testutils.reply_thread(self.thread).pk,
        )

        self.refresh_thread()
        self.assertEqual(self.thread.replies, 4)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'thread_url': other_thread.get_absolute_url(),
                'posts': posts,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # replies were moved
        self.refresh_thread()
        self.assertEqual(self.thread.replies, 0)

        other_thread = Thread.objects.get(pk=other_thread.pk)
        self.assertEqual(other_thread.post_set.filter(pk__in=posts).count(), 4)
        self.assertEqual(other_thread.replies, 4)
