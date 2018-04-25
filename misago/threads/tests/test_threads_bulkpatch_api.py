import json

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.models import Thread

from .test_threads_api import ThreadsApiTestCase


class ThreadsBulkPatchApiTestCase(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadsBulkPatchApiTestCase, self).setUp()

        self.threads = [
            testutils.post_thread(category=self.category),
            testutils.post_thread(category=self.category),
            testutils.post_thread(category=self.category),
        ]

        self.ids = [t.id for t in self.threads]

        self.api_link = reverse('misago:api:thread-list')

    def patch(self, api_link, ops):
        return self.client.patch(api_link, json.dumps(ops), content_type="application/json")



class BulkPatchSerializerTests(ThreadsBulkPatchApiTestCase):
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
                "Ensure this field has no more than 40 elements.",
            ],
            'ops': [
                "Ensure this field has no more than 10 elements.",
            ],
        })

    def test_threads_not_found(self):
        """api fails to find threads"""
        threads = [
            testutils.post_thread(category=self.category, is_hidden=True),
            testutils.post_thread(category=self.category, is_unapproved=True),
        ]

        response = self.patch(self.api_link, {
            'ids': [t.id for t in threads],
            'ops': [{}],
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail': 'NOT FOUND'})

    def test_ops_invalid(self):
        """api validates descriptions"""
        response = self.patch(self.api_link, {
            'ids': self.ids,
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


class ThreadAddAclApiTests(ThreadsBulkPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds current threads acl to response"""
        response = self.patch(self.api_link,
            {
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
        for i, thread_id in enumerate(self.ids):
            data = response_json[i]
            self.assertEqual(data['id'], str(thread_id))
            self.assertEqual(data['status'], '200')
            self.assertTrue(data['patch']['acl'])


class ThreadsBulkChangeTitleApiTests(ThreadsBulkPatchApiTestCase):
    def test_change_thread_title(self):
        """api changes thread title and resyncs the category"""
        self.override_acl({'can_edit_threads': 2})

        response = self.patch(
            self.api_link,
            {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'title',
                        'value': 'Changed the title!',
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': str(thread_id),
                'status': '200',
                'patch': {
                    'title': 'Changed the title!',
                }
            } for thread_id in self.ids
        ])

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertEqual(thread.title, 'Changed the title!')

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.last_thread_title, 'Changed the title!')

    def test_change_thread_title_no_permission(self):
        """api validates permission to change title, returns errors"""
        self.override_acl({'can_edit_threads': 0})

        response = self.patch(
            self.api_link,
            {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'title',
                        'value': 'Changed the title!',
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': str(thread_id),
                'status': '403',
                'detail': "You can't edit threads in this category.",
            } for thread_id in self.ids
        ])


class ThreadsBulkMoveApiTests(ThreadsBulkPatchApiTestCase):
    def setUp(self):
        super(ThreadsBulkMoveApiTests, self).setUp()

        Category(
            name='Category B',
            slug='category-b',
        ).insert_at(
            self.category,
            position='last-child',
            save=True,
        )
        self.category_b = Category.objects.get(slug='category-b')

    def override_other_acl(self, acl):
        other_category_acl = self.user.acl_cache['categories'][self.category.pk].copy()
        other_category_acl.update({
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
        })
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

    def test_move_thread(self):
        """api moves threads to other category and syncs both categories"""
        self.override_acl({'can_move_threads': True})
        self.override_other_acl({'can_start_threads': 2})

        response = self.patch(
            self.api_link,
            {
                'ids': self.ids,
                'ops': [
                    {
                        'op': 'replace',
                        'path': 'category',
                        'value': self.category_b.pk,
                    },
                    {
                        'op': 'replace',
                        'path': 'flatten-categories',
                        'value': None,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': str(thread_id),
                'status': '200',
                'patch': {
                    'category': self.category_b.pk,
                },
            } for thread_id in self.ids
        ])

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertEqual(thread.category_id, self.category_b.pk)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.threads, self.category.threads - 3)

        new_category = Category.objects.get(pk=self.category_b.pk)
        self.assertEqual(new_category.threads, 3)


class ThreadsBulksHideApiTests(ThreadsBulkPatchApiTestCase):
    def test_hide_thread(self):
        """api makes it possible to hide thread"""
        self.override_acl({'can_hide_threads': 1})

        response = self.patch(
            self.api_link,
            {
                'ids': self.ids,
                'ops': [
                    {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'id': str(thread_id),
                'status': '200',
                'patch': {
                    'is_hidden': True,
                },
            } for thread_id in self.ids
        ])

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertTrue(thread.is_hidden)

        category = Category.objects.get(pk=self.category.pk)
        self.assertNotIn(category.last_thread_id, self.ids)


class ThreadsBulksApproveApiTests(ThreadsBulkPatchApiTestCase):
    def test_approve_thread(self):
        """api approvse threads and syncs category"""
        for thread in self.threads:
            thread.first_post.is_unapproved = True
            thread.first_post.save()

            thread.synchronize()
            thread.save()

            self.assertTrue(thread.is_unapproved)
            self.assertTrue(thread.has_unapproved_posts)

        self.category.synchronize()
        self.category.save()

        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link,
            {
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
                'id': str(thread_id),
                'status': '200',
                'patch': {
                    'is_unapproved': False,
                    'has_unapproved_posts': False,
                },
            } for thread_id in self.ids
        ])

        for thread in Thread.objects.filter(id__in=self.ids):
            self.assertFalse(thread.is_unapproved)
            self.assertFalse(thread.has_unapproved_posts)

        category = Category.objects.get(pk=self.category.pk)
        self.assertIn(category.last_thread_id, self.ids)
