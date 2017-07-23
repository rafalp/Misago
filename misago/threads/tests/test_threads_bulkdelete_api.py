import json

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories import PRIVATE_THREADS_ROOT_NAME
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.models import Thread
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
        self.assertContains(response, "This action is not available to guests.", status_code=403)

    def test_delete_no_ids(self):
        """api requires ids to delete"""
        self.override_acl({
            'can_hide_own_threads': 0,
            'can_hide_threads': 0,
        })

        response = self.delete(self.api_link)
        self.assertContains(response, "You have to specify at least one thread to delete.", status_code=403)

    def test_validate_ids(self):
        """api validates that ids are list of ints"""
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        response = self.delete(self.api_link, True)
        self.assertContains(response, "One or more thread ids received were invalid.", status_code=403)

        response = self.delete(self.api_link, 'abbss')
        self.assertContains(response, "One or more thread ids received were invalid.", status_code=403)

        response = self.delete(self.api_link, [1, 2, 3, 'a', 'b', 'x'])
        self.assertContains(response, "One or more thread ids received were invalid.", status_code=403)

    def test_validate_ids_length(self):
        """api validates that ids are list of ints"""
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 2,
        })

        response = self.delete(self.api_link, list(range(100)))
        self.assertContains(response, "No more than 40 threads can be deleted at single time.", status_code=403)

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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        # unapproved thread wasn't deleted
        Thread.objects.get(pk=unapproved_thread.pk)

        deleted_threads = [self.threads[0], self.threads[2]]
        for thread in deleted_threads:
            with self.assertRaises(Thread.DoesNotExist):
                Thread.objects.get(pk=thread.pk)

        category = Category.objects.get(pk=self.category.pk)
        self.assertNotIn(category.last_thread_id, threads_ids)

    def test_delete_other_user_thread_no_permission(self):
        """api valdiates if user can delete other users threads"""
        self.override_acl({
            'can_hide_own_threads': 2,
            'can_hide_threads': 0,
        })

        other_thread = self.threads[1]

        response = self.delete(self.api_link, [p.id for p in self.threads])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), [
            {
                'thread': {
                    'id': other_thread.pk,
                    'title': other_thread.title
                },
                'error': "You can't delete other users theads in this category."
            }
        ])

        Thread.objects.get(pk=self.threads[1].pk)

        deleted_threads = [self.threads[0], self.threads[2]]
        for thread in deleted_threads:
            with self.assertRaises(Thread.DoesNotExist):
                Thread.objects.get(pk=thread.pk)

        category = Category.objects.get(pk=self.category.pk)
        self.assertEqual(category.last_thread_id, self.threads[1].pk)

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
        self.assertEqual(response.json(), [
            {
                'thread': {
                    'id': thread.pk,
                    'title': thread.title
                },
                'error': "This category is closed. You can't delete threads in it."
            } for thread in sorted(self.threads, key=lambda i: i.pk, reverse=True)
        ])

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
        self.assertEqual(response.json(), [
            {
                'thread': {
                    'id': closed_thread.pk,
                    'title': closed_thread.title
                },
                'error': "This thread is closed. You can't delete it."
            }
        ])

    def test_delete_private_thread(self):
        """attempt to delete private thread fails"""
        private_thread = self.threads[0]

        private_thread.category = Category.objects.get(
            tree_id=trees_map.get_tree_id_for_root(PRIVATE_THREADS_ROOT_NAME),
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        Thread.objects.get(pk=private_thread.pk)

        deleted_threads = [self.threads[1], self.threads[2]]
        for thread in deleted_threads:
            with self.assertRaises(Thread.DoesNotExist):
                Thread.objects.get(pk=thread.pk)

        category = Category.objects.get(pk=self.category.pk)
        self.assertNotIn(category.last_thread_id, threads_ids)
