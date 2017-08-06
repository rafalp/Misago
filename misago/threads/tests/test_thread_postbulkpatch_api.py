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

    def test_invalid_id(self):
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
        self.assertEqual(response.json(), [
            {'id': self.ids[0], 'detail': ['undefined op']},
        ])

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
        """api adds current event's acl to response"""
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
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertTrue(response_json[i]['acl'])

    def test_add_acl_false(self):
        """if value is false, api won't add acl to the response, but will set empty key"""
        response = self.patch(self.api_link, {
            'ids': self.ids,
            'ops': [
                {
                    'op': 'add',
                    'path': 'acl',
                    'value': False,
                },
            ]
        })
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertIsNone(response_json[i]['acl'])


class BulkPostProtectApiTests(ThreadPostBulkPatchApiTestCase):
    def test_protect_post(self):
        """api makes it possible to protect post"""
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

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertTrue(response_json[i]['is_protected'])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_protected)

    def test_unprotect_post(self):
        """api makes it possible to unprotect protected post"""
        self.override_acl({
            'can_protect_posts': 1,
            'can_edit_posts': 2,
        })

        for post in self.posts:
            post.is_protected = True
            post.save()

        response = self.patch(
            self.api_link, {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'is-protected',
                        'value': False,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertFalse(response_json[i]['is_protected'])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_protected)

    def test_protect_post_no_permission(self):
        """api validates permission to protect post"""
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
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["You can't protect posts in this category."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_protected)

    def test_unprotect_post_no_permission(self):
        """api validates permission to unprotect post"""
        for post in self.posts:
            post.is_protected = True
            post.save()

        self.override_acl({'can_protect_posts': 0})

        response = self.patch(
            self.api_link, {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'is-protected',
                        'value': False,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["You can't protect posts in this category."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_protected)

    def test_protect_post_not_editable(self):
        """api validates if we can edit post we want to protect"""
        self.override_acl({
            'can_protect_posts': 1,
            'can_edit_posts': 0,
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
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["You can't protect posts you can't edit."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_protected)

    def test_unprotect_post_not_editable(self):
        """api validates if we can edit post we want to protect"""
        for post in self.posts:
            post.is_protected = True
            post.save()


        self.override_acl({
            'can_protect_posts': 1,
            'can_edit_posts': 0,
        })

        response = self.patch(
            self.api_link, {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'is-protected',
                        'value': False,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["You can't protect posts you can't edit."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_protected)


class PostsApproveApiTests(ThreadPostBulkPatchApiTestCase):
    def test_approve_post(self):
        """api makes it possible to approve post"""
        for post in self.posts:
            post.is_unapproved = True
            post.save()

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

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertFalse(response_json[i]['is_unapproved'])

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_unapproved)

    def test_unapprove_post(self):
        """unapproving posts is not supported by api"""
        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'is-unapproved',
                        'value': True,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["Content approval can't be reversed."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertFalse(post.is_unapproved)

    def test_approve_post_no_permission(self):
        """api validates approval permission"""
        for post in self.posts:
            post.poster = self.user
            post.is_unapproved = True
            post.save()

        self.override_acl({'can_approve_content': 0})

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
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["You can't approve posts in this category."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_unapproved)

    def test_approve_post_closed_thread_no_permission(self):
        """api validates approval permission in closed threads"""
        for post in self.posts:
            post.is_unapproved = True
            post.save()

        self.thread.is_closed = True
        self.thread.save()

        self.override_acl({
            'can_approve_content': 1,
            'can_close_threads': 0,
        })

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
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["This thread is closed. You can't approve posts in it."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_unapproved)

    def test_approve_post_closed_category_no_permission(self):
        """api validates approval permission in closed categories"""
        for post in self.posts:
            post.is_unapproved = True
            post.save()

        self.category.is_closed = True
        self.category.save()

        self.override_acl({
            'can_approve_content': 1,
            'can_close_threads': 0,
        })

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
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["This category is closed. You can't approve posts in it."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_unapproved)

    def test_approve_first_post(self):
        """api approve first post fails"""
        for post in self.posts:
            post.is_unapproved = True
            post.save()

        self.thread.set_first_post(self.posts[0])
        self.thread.save()

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
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json[0], {
            'id': self.posts[0].id,
            'detail': ["You can't approve thread's first post."],
        })

        for post in Post.objects.filter(id__in=self.ids):
            if post.id == self.ids[0]:
                self.assertTrue(post.is_unapproved)
            else:
                self.assertFalse(post.is_unapproved)

    def test_approve_hidden_post(self):
        """api approve hidden post fails"""
        for post in self.posts:
            post.is_unapproved = True
            post.is_hidden = True
            post.save()

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
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        for i, post in enumerate(self.posts):
            self.assertEqual(response_json[i]['id'], post.id)
            self.assertEqual(
                response_json[i]['detail'],
                ["You can't approve posts the content you can't see."],
            )

        for post in Post.objects.filter(id__in=self.ids):
            self.assertTrue(post.is_unapproved)
