import json

from django.urls import reverse
from django.utils import six

from misago.acl.testutils import override_acl
from misago.categories.models import PRIVATE_THREADS_ROOT, Category
from misago.threads import testutils
from misago.threads.models import Thread
from misago.threads.serializers.moderation import THREADS_LIMIT
from misago.threads.threadtypes import trees_map

from .test_threads_api import ThreadsApiTestCase


class ThreadsBulkDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadsBulkDeleteApiTests, self).setUp()

        self.api_link = reverse('misago:api:thread-list')

        self.threads = [
            testutils.post_thread(
                category=self.category,
                poster=self.user,
            ),
            testutils.post_thread(category=self.category),
            testutils.post_thread(
                category=self.category,
                poster=self.user,
            ),
        ]

    def delete(self, url, data=None):
        return self.client.delete(url, json.dumps(data), content_type="application/json")

    def test_delete_anonymous(self):
        """anonymous users can't bulk delete threads"""
        self.logout_user()

        response = self.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This action is not available to guests.",
        })

    def test_delete_no_ids(self):
        """api requires ids to delete"""
        self.override_acl({
            'can_hide_own_threads': 0,
            'can_hide_threads': 0,
        })

        response = self.delete(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': ["You have to specify at least one thread to delete."],
        })

    def test_validate_ids(self):
        """api validates that ids are list of ints"""
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        response = self.delete(self.api_link, True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': ['Expected a list of items but got type "bool".'],
        })

        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        response = self.delete(self.api_link, 'abbss')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': [
                'Expected a list of items but got type "{}".'.format(six.text_type.__name__)
            ],
        })
        
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        response = self.delete(self.api_link, [1, 2, 3, 'a', 'b', 'x'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': ["One or more thread ids received were invalid."],
        })

    def test_validate_ids_length(self):
        """api validates that ids are list of ints"""
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        response = self.delete(self.api_link, list(range(THREADS_LIMIT + 1)))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': [
                "No more than {} threads can be deleted at single time.".format(THREADS_LIMIT)
            ],
        })

    def test_validate_thread_visibility(self):
        """api valdiates if user can see deleted thread"""
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        unapproved_thread = self.threads[1]

        unapproved_thread.is_unapproved = True
        unapproved_thread.save()

        threads_ids = [p.id for p in self.threads]

        response = self.delete(self.api_link, threads_ids)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': ["One or more threads to delete could not be found."],
        })

        # no thread was deleted
        for thread in self.threads:
            Thread.objects.get(pk=thread.pk)

    def test_delete_other_user_thread_no_permission(self):
        """api valdiates if user can delete other users threads"""
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 0,
        })

        other_thread = self.threads[1]

        response = self.delete(self.api_link, [p.id for p in self.threads])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': {
                'details': [
                    {
                        'thread': {
                            'id': str(other_thread.pk),
                            'title': other_thread.title
                        },
                        'error': "You can't delete other users theads in this category.",
                    },
                ],
            },
        })

        # no threads are removed on failed attempt
        for thread in self.threads:
            Thread.objects.get(pk=thread.pk)

    def test_delete_thread_closed_category_no_permission(self):
        """api tests category's closed state"""
        self.category.is_closed = True
        self.category.save()

        self.override_acl({
            'can_hide_threads': 2,
            'can_hide_own_threads': 2,
            'can_close_threads': False,
        })

        response = self.delete(self.api_link, [p.id for p in self.threads])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': {
                'details': [
                    {
                        'thread': {
                            'id': str(thread.pk),
                            'title': thread.title,
                        },
                        'error': "This category is closed. You can't delete threads in it.",
                    } for thread in reversed(self.threads)
                ],
            },
        })

    def test_delete_thread_closed_no_permission(self):
        """api tests thread's closed state"""
        closed_thread = self.threads[1]
        closed_thread.is_closed = True
        closed_thread.save()

        self.override_acl({
            'can_hide_threads': 2,
            'can_hide_own_threads': 2,
            'can_close_threads': False,
        })

        response = self.delete(self.api_link, [p.id for p in self.threads])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': {
                'details': [
                    {
                        'thread': {
                            'id': str(closed_thread.pk),
                            'title': closed_thread.title,
                        },
                        'error': "This thread is closed. You can't delete it.",
                    },
                ],
            },
        })

    def test_delete_private_thread(self):
        """attempt to delete private thread fails"""
        private_thread = self.threads[0]

        private_thread.category = Category.objects.get(
            tree_id=trees_map.get_tree_id_for_root(PRIVATE_THREADS_ROOT),
        )
        private_thread.save()

        private_thread.threadparticipant_set.create(
            user=self.user,
            is_owner=True,
        )

        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        threads_ids = [p.id for p in self.threads]

        response = self.delete(self.api_link, threads_ids)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'threads': ["One or more threads to delete could not be found."],
        })

        Thread.objects.get(pk=private_thread.pk)
