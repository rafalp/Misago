# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.api.postendpoints.split import SPLIT_LIMIT
from misago.threads.models import Thread
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadPostSplitApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadPostSplitApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.posts = [
            testutils.reply_thread(self.thread).pk, testutils.reply_thread(self.thread).pk
        ]

        self.api_link = reverse(
            'misago:api:thread-post-split', kwargs={
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
        """you need to authenticate to split posts"""
        self.logout_user()

        response = self.client.post(self.api_link, json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_no_permission(self):
        """api validates permission to split"""
        self.override_acl({'can_move_posts': 0})

        response = self.client.post(self.api_link, json.dumps({}), content_type="application/json")
        self.assertContains(response, "You can't split posts from this thread.", status_code=403)

    def test_empty_data(self):
        """api handles empty data"""
        response = self.client.post(self.api_link)
        self.assertContains(
            response, "You have to specify at least one post to split.", status_code=400
        )

    def test_no_posts_ids(self):
        """api rejects no posts ids"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "You have to specify at least one post to split.", status_code=400
        )

    def test_invalid_posts_data(self):
        """api handles invalid data"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': 'string',
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
                'posts': [1, 2, 'string'],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more post ids received were invalid.", status_code=400
        )

    def test_split_limit(self):
        """api rejects more posts than split limit"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': list(range(SPLIT_LIMIT + 1)),
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "No more than {} posts can be split".format(SPLIT_LIMIT), status_code=400
        )

    def test_split_invisible(self):
        """api validates posts visibility"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [testutils.reply_thread(self.thread, is_unapproved=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more posts to split could not be found.", status_code=400
        )

    def test_split_event(self):
        """api rejects events split"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [testutils.reply_thread(self.thread, is_event=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(response, "Events can't be split.", status_code=400)

    def test_split_first_post(self):
        """api rejects first post split"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [self.thread.first_post_id],
            }),
            content_type="application/json",
        )
        self.assertContains(response, "You can't split thread's first post.", status_code=400)

    def test_split_hidden_posts(self):
        """api recjects attempt to split urneadable hidden post"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [testutils.reply_thread(self.thread, is_hidden=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "You can't split posts the content you can't see.", status_code=400
        )

    def test_split_other_thread_posts(self):
        """api recjects attempt to split other thread's post"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': [testutils.reply_thread(other_thread, is_hidden=True).pk],
            }),
            content_type="application/json",
        )
        self.assertContains(
            response, "One or more posts to split could not be found.", status_code=400
        )

    def test_split_empty_new_thread_data(self):
        """api handles empty form data"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ['This field is required.'],
                'category': ['This field is required.'],
            }
        )

    def test_split_invalid_final_title(self):
        """api rejects split because final thread title was invalid"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': '$$$',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_split_invalid_category(self):
        """api rejects split because final category was invalid"""
        self.override_other_acl({'can_see': 0})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Valid thread title',
                'category': self.category_b.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'category': ["Requested category could not be found."],
            }
        )

    def test_split_unallowed_start_thread(self):
        """api rejects split because category isn't allowing starting threads"""
        self.override_acl({'can_start_threads': 0})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Valid thread title',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'category': ["You can't create new threads in selected category."],
            }
        )

    def test_split_invalid_weight(self):
        """api rejects split because final weight was invalid"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Valid thread title',
                'category': self.category.id,
                'weight': 4,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'weight': ["Ensure this value is less than or equal to 2."],
            }
        )

    def test_split_unallowed_global_weight(self):
        """api rejects split because global weight was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Valid thread title',
                'category': self.category.id,
                'weight': 2,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'weight': ["You don't have permission to pin threads globally in this category."],
            }
        )

    def test_split_unallowed_local_weight(self):
        """api rejects split because local weight was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Valid thread title',
                'category': self.category.id,
                'weight': 1,
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'weight': ["You don't have permission to pin threads in this category."],
            }
        )

    def test_split_allowed_local_weight(self):
        """api allows local weight"""
        self.override_acl({'can_pin_threads': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': '$$$',
                'category': self.category.id,
                'weight': 1,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_split_allowed_global_weight(self):
        """api allows global weight"""
        self.override_acl({'can_pin_threads': 2})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': '$$$',
                'category': self.category.id,
                'weight': 2,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_split_unallowed_close(self):
        """api rejects split because closing thread was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Valid thread title',
                'category': self.category.id,
                'is_closed': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'is_closed': ["You don't have permission to close threads in this category."],
            }
        )

    def test_split_with_close(self):
        """api allows for closing thread"""
        self.override_acl({'can_close_threads': True})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': '$$$',
                'category': self.category.id,
                'weight': 0,
                'is_closed': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_split_unallowed_hidden(self):
        """api rejects split because hidden thread was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Valid thread title',
                'category': self.category.id,
                'is_hidden': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'is_hidden': ["You don't have permission to hide threads in this category."],
            }
        )

    def test_split_with_hide(self):
        """api allows for hiding thread"""
        self.override_acl({'can_hide_threads': True})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': '$$$',
                'category': self.category.id,
                'weight': 0,
                'is_hidden': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_split(self):
        """api splits posts to new thread"""
        self.refresh_thread()
        self.assertEqual(self.thread.replies, 2)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Split thread.',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # thread was created
        split_thread = self.category.thread_set.get(slug='split-thread')
        self.assertEqual(split_thread.replies, 1)

        # posts were removed from old thread
        self.refresh_thread()
        self.assertEqual(self.thread.replies, 0)

        # posts were moved to new thread
        self.assertEqual(split_thread.post_set.filter(pk__in=self.posts).count(), 2)

    def test_split_kitchensink(self):
        """api splits posts with kitchensink"""
        self.refresh_thread()
        self.assertEqual(self.thread.replies, 2)

        self.override_other_acl({
            'can_start_threads': 2,
            'can_close_threads': True,
            'can_hide_threads': True,
            'can_pin_threads': 2,
        })

        response = self.client.post(
            self.api_link,
            json.dumps({
                'posts': self.posts,
                'title': 'Split thread',
                'category': self.category_b.id,
                'weight': 2,
                'is_closed': 1,
                'is_hidden': 1,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # thread was created
        split_thread = self.category_b.thread_set.get(slug='split-thread')
        self.assertEqual(split_thread.replies, 1)
        self.assertEqual(split_thread.weight, 2)
        self.assertTrue(split_thread.is_closed)
        self.assertTrue(split_thread.is_hidden)

        # posts were removed from old thread
        self.refresh_thread()
        self.assertEqual(self.thread.replies, 0)

        # posts were moved to new thread
        self.assertEqual(split_thread.post_set.filter(pk__in=self.posts).count(), 2)
