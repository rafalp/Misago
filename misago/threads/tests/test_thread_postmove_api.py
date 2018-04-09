# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.readtracker import poststracker
from misago.threads import testutils
from misago.threads.models import Thread
from misago.threads.serializers.moderation import POSTS_LIMIT
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

    def override_other_acl(self, extra_acl=None):
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

        if extra_acl:
            other_category_acl.update(extra_acl)

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
        self.assertEqual(response.json(), {
            'detail': "This action is not available to guests.",
        })

    def test_invalid_data(self):
        """api handles post that is invalid type"""
        self.override_acl()
        response = self.client.post(self.api_link, '[]', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["Invalid data. Expected a dictionary, but got list."],
        })

        self.override_acl()
        response = self.client.post(self.api_link, '123', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["Invalid data. Expected a dictionary, but got int."],
        })

        self.override_acl()
        response = self.client.post(self.api_link, '"string"', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["Invalid data. Expected a dictionary, but got str."],
        })

        self.override_acl()
        response = self.client.post(self.api_link, 'malformed', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'detail': "JSON parse error - Expecting value: line 1 column 1 (char 0)",
        })

    def test_no_permission(self):
        """api validates permission to move"""
        self.override_acl({'can_move_posts': 0})

        response = self.client.post(self.api_link, json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't move posts in this thread.",
        })

    def test_move_no_new_thread_url(self):
        """api validates if new thread url was given"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_thread': ["Enter link to new thread."],
            'posts': ["You have to specify at least one post to move."],
        })

    def test_invalid_new_thread_url(self):
        """api validates new thread url"""
        response = self.client.post(self.api_link, {
            'new_thread': self.user.get_absolute_url(),
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_thread': ["This is not a valid thread link."],
            'posts': ["You have to specify at least one post to move."],
        })

    def test_current_new_thread_url(self):
        """api validates if new thread url points to current thread"""
        response = self.client.post(
            self.api_link, {
                'new_thread': self.thread.get_absolute_url(),
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_thread': ["Thread to move posts to is same as current one."],
            'posts': ["You have to specify at least one post to move."],
        })

    def test_other_thread_exists(self):
        """api validates if other thread exists"""
        self.override_other_acl()

        other_thread = testutils.post_thread(self.category_b)
        other_new_thread = other_thread.get_absolute_url()
        other_thread.delete()

        response = self.client.post(self.api_link, {
            'new_thread': other_new_thread,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_thread': [
                "The thread you have entered link to doesn't exist or you don't have permission "
                "to see it."
            ],
            'posts': ["You have to specify at least one post to move."],
        })

    def test_other_thread_is_invisible(self):
        """api validates if other thread is visible"""
        self.override_other_acl({'can_see': 0})

        other_thread = testutils.post_thread(self.category_b)

        response = self.client.post(
            self.api_link, {
                'new_thread': other_thread.get_absolute_url(),
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_thread': [
                "The thread you have entered link to doesn't exist or you don't have permission "
                "to see it."
            ],
            'posts': ["You have to specify at least one post to move."],
        })

    def test_other_thread_isnt_replyable(self):
        """api validates if other thread can be replied"""
        self.override_other_acl({'can_reply_threads': 0})

        other_thread = testutils.post_thread(self.category_b)

        response = self.client.post(
            self.api_link, {
                'new_thread': other_thread.get_absolute_url(),
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_thread': [
                "You can't move posts to threads you can't reply."
            ],
            'posts': ["You have to specify at least one post to move."],
        })

    def test_empty_data(self):
        """api handles empty data"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_thread': ["Enter link to new thread."],
            'posts': ["You have to specify at least one post to move."],
        })

    def test_empty_posts_data_json(self):
        """api handles empty json data"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["You have to specify at least one post to move."],
        })

    def test_no_posts_ids(self):
        """api rejects no posts ids"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["You have to specify at least one post to move."],
        })

    def test_invalid_posts_data(self):
        """api handles invalid data"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': 'string',
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ['Expected a list of items but got type "str".'],
        })

    def test_invalid_posts_ids(self):
        """api handles invalid post id"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [1, 2, 'string'],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["One or more post ids received were invalid."],
        })

    def test_move_limit(self):
        """api rejects more posts than move limit"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': list(range(POSTS_LIMIT + 1)),
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["No more than {} posts can be moved at single time.".format(POSTS_LIMIT)],
        })

    def test_move_invisible(self):
        """api validates posts visibility"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread, is_unapproved=True).pk],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["One or more posts to move could not be found."],
        })

    def test_move_other_thread_posts(self):
        """api recjects attempt to move other thread's post"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(other_thread, is_hidden=True).pk],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["One or more posts to move could not be found."],
        })

    def test_move_event(self):
        """api rejects events move"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread, is_event=True).pk],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["Events can't be moved."],
        })

    def test_move_first_post(self):
        """api rejects first post move"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [self.thread.first_post_id],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["You can't move thread's first post."],
        })

    def test_move_hidden_posts(self):
        """api recjects attempt to move urneadable hidden post"""
        other_thread = testutils.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread, is_hidden=True).pk],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["You can't move posts the content you can't see."],
        })

    def test_move_posts_closed_thread_no_permission(self):
        """api recjects attempt to move posts from closed thread"""
        other_thread = testutils.post_thread(self.category)

        self.thread.is_closed = True
        self.thread.save()

        self.override_acl({'can_close_threads': 0})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread).pk],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["This thread is closed. You can't move posts in it."],
        })

    def test_move_posts_closed_category_no_permission(self):
        """api recjects attempt to move posts from closed thread"""
        other_thread = testutils.post_thread(self.category_b)

        self.category.is_closed = True
        self.category.save()

        self.override_acl({'can_close_threads': 0})
        self.override_other_acl({'can_reply_threads': 1})

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [testutils.reply_thread(self.thread).pk],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'posts': ["This category is closed. You can't move posts in it."],
        })

    def test_move_posts(self):
        """api moves posts to other thread"""
        self.override_other_acl({'can_reply_threads': 1})

        other_thread = testutils.post_thread(self.category_b)

        posts = (
            testutils.reply_thread(self.thread).pk,
            testutils.reply_thread(self.thread).pk,
            testutils.reply_thread(self.thread).pk,
            testutils.reply_thread(self.thread).pk,
        )

        self.refresh_thread()
        self.assertEqual(self.thread.replies, 4)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
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

    def test_move_best_answer(self):
        """api moves best answer to other thread"""
        self.override_other_acl({'can_reply_threads': 1})

        other_thread = testutils.post_thread(self.category_b)
        best_answer = testutils.reply_thread(self.thread)

        self.thread.set_best_answer(self.user, best_answer)
        self.thread.synchronize()
        self.thread.save()

        self.refresh_thread()
        self.assertEqual(self.thread.best_answer, best_answer)
        self.assertEqual(self.thread.replies, 1)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [best_answer.pk],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # best_answer was moved and unmarked
        self.refresh_thread()
        self.assertEqual(self.thread.replies, 0)
        self.assertIsNone(self.thread.best_answer)

        other_thread = Thread.objects.get(pk=other_thread.pk)
        self.assertEqual(other_thread.replies, 1)
        self.assertIsNone(other_thread.best_answer)

    def test_move_posts_reads(self):
        """api moves posts reads together with posts"""
        self.override_other_acl({'can_reply_threads': 1})

        other_thread = testutils.post_thread(self.category_b)

        posts = [
            testutils.reply_thread(self.thread),
            testutils.reply_thread(self.thread),
        ]

        self.refresh_thread()
        self.assertEqual(self.thread.replies, 2)

        poststracker.save_read(self.user, self.thread.first_post)
        for post in posts:
            poststracker.save_read(self.user, post)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'new_thread': other_thread.get_absolute_url(),
                'posts': [p.pk for p in posts],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        other_thread = Thread.objects.get(pk=other_thread.pk)

        # postreads were removed
        postreads = self.user.postread_set.order_by('id')

        postreads_threads = list(postreads.values_list('thread_id', flat=True))
        self.assertEqual(postreads_threads, [self.thread.pk])

        postreads_categories = list(postreads.values_list('category_id', flat=True))
        self.assertEqual(postreads_categories, [self.category.pk])
