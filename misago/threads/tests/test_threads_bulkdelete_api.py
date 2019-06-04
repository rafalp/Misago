import json

from django.urls import reverse

from .. import test
from ...categories import PRIVATE_THREADS_ROOT_NAME
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ..models import Thread
from ..test import patch_category_acl
from ..threadtypes import trees_map
from .test_threads_api import ThreadsApiTestCase


class ThreadsBulkDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()

        self.api_link = reverse("misago:api:thread-list")

        self.threads = [
            test.post_thread(category=self.category, poster=self.user),
            test.post_thread(category=self.category),
            test.post_thread(category=self.category, poster=self.user),
        ]

    def delete(self, url, data=None):
        return self.client.delete(
            url, json.dumps(data), content_type="application/json"
        )

    def test_delete_anonymous(self):
        """anonymous users can't bulk delete threads"""
        self.logout_user()

        response = self.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    @patch_category_acl({"can_hide_threads": 2, "can_hide_own_threads": 2})
    def test_delete_no_ids(self):
        """api requires ids to delete"""
        response = self.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one thread to delete."},
        )

    @patch_category_acl({"can_hide_threads": 2, "can_hide_own_threads": 2})
    def test_validate_ids(self):
        response = self.delete(self.api_link, True)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "bool".'}
        )

        response = self.delete(self.api_link, "abbss")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "str".'}
        )

        response = self.delete(self.api_link, [1, 2, 3, "a", "b", "x"])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "One or more thread ids received were invalid."}
        )

    @override_dynamic_settings(threads_per_page=4)
    @patch_category_acl({"can_hide_threads": 2, "can_hide_own_threads": 2})
    def test_validate_ids_length(self):
        """api validates that ids are list of ints"""
        response = self.delete(self.api_link, list(range(5)))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "No more than 4 threads can be deleted at a single time."},
        )

    @patch_category_acl({"can_hide_threads": 2, "can_hide_own_threads": 2})
    def test_validate_thread_visibility(self):
        """api valdiates if user can see deleted thread"""
        unapproved_thread = self.threads[1]

        unapproved_thread.is_unapproved = True
        unapproved_thread.save()

        threads_ids = [p.id for p in self.threads]

        response = self.delete(self.api_link, threads_ids)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more threads to delete could not be found."},
        )

        # no thread was deleted
        for thread in self.threads:
            Thread.objects.get(pk=thread.pk)

    @patch_category_acl({"can_hide_threads": 0, "can_hide_own_threads": 2})
    def test_delete_other_user_thread_no_permission(self):
        """api valdiates if user can delete other users threads"""
        other_thread = self.threads[1]

        response = self.delete(self.api_link, [p.id for p in self.threads])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            [
                {
                    "thread": {"id": other_thread.pk, "title": other_thread.title},
                    "error": "You can't delete other users theads in this category.",
                }
            ],
        )

        # no threads are removed on failed attempt
        for thread in self.threads:
            Thread.objects.get(pk=thread.pk)

    @patch_category_acl(
        {"can_hide_threads": 2, "can_hide_own_threads": 2, "can_close_threads": False}
    )
    def test_delete_thread_closed_category_no_permission(self):
        """api tests category's closed state"""
        self.category.is_closed = True
        self.category.save()

        response = self.delete(self.api_link, [p.id for p in self.threads])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            [
                {
                    "thread": {"id": thread.pk, "title": thread.title},
                    "error": "This category is closed. You can't delete threads in it.",
                }
                for thread in sorted(self.threads, key=lambda i: i.pk)
            ],
        )

    @patch_category_acl(
        {"can_hide_threads": 2, "can_hide_own_threads": 2, "can_close_threads": False}
    )
    def test_delete_thread_closed_no_permission(self):
        """api tests thread's closed state"""
        closed_thread = self.threads[1]
        closed_thread.is_closed = True
        closed_thread.save()

        response = self.delete(self.api_link, [p.id for p in self.threads])

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            [
                {
                    "thread": {"id": closed_thread.pk, "title": closed_thread.title},
                    "error": "This thread is closed. You can't delete it.",
                }
            ],
        )

    @patch_category_acl({"can_hide_threads": 2, "can_hide_own_threads": 2})
    def test_delete_private_thread(self):
        """attempt to delete private thread fails"""
        private_thread = self.threads[0]

        private_thread.category = Category.objects.get(
            tree_id=trees_map.get_tree_id_for_root(PRIVATE_THREADS_ROOT_NAME)
        )
        private_thread.save()

        private_thread.threadparticipant_set.create(user=self.user, is_owner=True)

        threads_ids = [p.id for p in self.threads]

        response = self.delete(self.api_link, threads_ids)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more threads to delete could not be found."},
        )

        Thread.objects.get(pk=private_thread.pk)
