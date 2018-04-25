# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.models import Post, Thread
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadPostBulkPatchApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadPostBulkPatchApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.posts = [
            testutils.reply_thread(self.thread, poster=self.user),
            testutils.reply_thread(self.thread),
            testutils.reply_thread(self.thread, poster=self.user),
        ]

        self.ids = [p.id for p in self.posts]

        self.api_link = reverse(
            'misago:api:thread-post-list',
            kwargs={
                'thread_pk': self.thread.pk,
            }
        )

    def patch(self, api_link, ops):
        return self.client.patch(api_link, json.dumps(ops), content_type="application/json")

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


class BulkPatchSerializerTests(ThreadPostBulkPatchApiTestCase):
    def test_invalid_input_type(self):
        """api rejects invalid input type"""
        response = self.patch(self.api_link, [1, 2, 3])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': [
                "Invalid data. Expected a dictionary, but got list.",
            ],
        })

    def test_missing_input_keys(self):
        """api rejects input with missing keys"""
        response = self.patch(self.api_link, {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'ids': [
                "This field is required.",
            ],
            'ops': [
                "This field is required.",
            ],
        })

    def test_empty_input_keys(self):
        """api rejects input with empty keys"""
        response = self.patch(self.api_link, {
            'ids': [],
            'ops': [],
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'ids': [
                "Ensure this field has at least 1 elements.",
            ],
            'ops': [
                "Ensure this field has at least 1 elements.",
            ],
        })

    def test_invalid_input_keys(self):
        """api rejects input with invalid keys"""
        response = self.patch(self.api_link, {
            'ids': ['a'],
            'ops': [1],
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'ids': [
                "A valid integer is required.",
            ],
            'ops': [
                'Expected a dictionary of items but got type "int".',
            ],
        })

    def test_too_small_id(self):
        """api rejects input with implausiple id"""
        response = self.patch(self.api_link, {
            'ids': [0],
            'ops': [{}],
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'ids': [
                "Ensure this value is greater than or equal to 1.",
            ],
        })

    def test_too_large_input(self):
        """api rejects too large input"""
        response = self.patch(self.api_link, {
            'ids': [i + 1 for i in range(200)],
            'ops': [{} for i in range(200)],
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'ids': [
                "Ensure this field has no more than 24 elements.",
            ],
            'ops': [
                "Ensure this field has no more than 10 elements.",
            ],
        })

    def test_posts_not_found(self):
        """api fails to find posts"""
        posts = [
            testutils.reply_thread(self.thread, is_hidden=True),
            testutils.reply_thread(self.thread, is_unapproved=True),
        ]

        response = self.patch(self.api_link, {
            'ids': [p.id for p in posts],
            'ops': [{}],
        })

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "One or more posts to update could not be found.",
        })

    def test_ops_invalid(self):
        """api validates descriptions"""
        response = self.patch(self.api_link, {
            'ids': self.ids[:1],
            'ops': [{}],
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ['"op" parameter must be defined.'],
        })

    def test_anonymous_user(self):
        """anonymous users can't use bulk actions"""
        self.logout_user()

        response = self.patch(self.api_link, {
            'ids': self.ids[:1],
            'ops': [{}],
        })
        self.assertEqual(response.status_code, 403)

    def test_events(self):
        """cant use bulk actions for events"""
        for post in self.posts:
            post.is_event = True
            post.save()

        response = self.patch(self.api_link, {
            'ids': self.ids,
            'ops': [{}],
        })

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "One or more posts to update could not be found.",
        })


class PostsAddAclApiTests(ThreadPostBulkPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds posts acls to response"""
        response = self.patch(self.api_link, {
            'ids': self.ids,
            'ops': [
                {
                    'op': 'add',
                    'path': 'acl',
                    'value': True,
                },
            ]
        })
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, post_id in enumerate(self.ids):
            data = response_json[i]
            self.assertEqual(data['id'], str(post_id))
            self.assertEqual(data['status'], '200')
            self.assertTrue(data['patch']['acl'])


class BulkPostProtectApiTests(ThreadPostBulkPatchApiTestCase):
    def test_protect_post(self):
        """api makes it possible to protect posts"""
        self.override_acl({
            'can_protect_posts': 1,
            'can_edit_posts': 2,
        })

        response = self.patch(
            self.api_link, {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'is-protected',
                        'value': True,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': str(post_id),
                'status': '200',
                'patch': {
                    'is_protected': True,
                },
            } for post_id in self.ids
        ])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_protected)

    def test_protect_post_no_permission(self):
        """api validates permission to protect posts and returns errors"""
        self.override_acl({'can_protect_posts': 0})

        response = self.patch(
            self.api_link, {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'is-protected',
                        'value': True,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': str(post_id),
                'status': '403',
                'detail': "You can't protect posts in this category.",
            } for post_id in self.ids
        ])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_protected)


class BulkPostsApproveApiTests(ThreadPostBulkPatchApiTestCase):
    def test_approve_post(self):
        """api resyncs thread and categories on posts approval"""
        for post in self.posts:
            post.is_unapproved = True
            post.save()

        self.thread.synchronize()
        self.thread.save()

        self.assertNotIn(self.thread.last_post_id, self.ids)

        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'is-unapproved',
                        'value': False,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': str(post_id),
                'status': '200',
                'patch': {
                    'is_unapproved': False,
                },
            } for post_id in self.ids
        ])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_unapproved)

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertIn(thread.last_post_id, self.ids)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.posts, 4)
