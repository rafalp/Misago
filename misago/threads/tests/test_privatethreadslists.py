from django.urls import reverse

from misago.acl.testutils import override_acl

from .. import testutils
from ..participants import add_owner
from .test_privatethreads_api import PrivateThreadsApiTestCase


class PrivateThreadsApiTests(PrivateThreadsApiTestCase):
    def setUp(self):
        super(PrivateThreadsApiTests, self).setUp()

        self.api_link = reverse('misago:api:private-thread-list')

    def test_unauthenticated(self):
        """api requires user to sign in and be able to access it"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertContains(response, "sign in to use private threads", status_code=403)

    def test_no_permission(self):
        """api requires user to have permission to be able to access it"""
        override_acl(self.user, {
            'can_use_private_threads': 0
        })

        response = self.client.get(self.api_link)
        self.assertContains(response, "can't use private threads", status_code=403)

    def test_empty_list(self):
        """api has no showstoppers on returning empty list"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['count'], 0)

    def test_thread_visibility(self):
        """only participated threads are returned by private threads api"""
        visible = testutils.post_thread(category=self.category, poster=self.user)
        hidden = testutils.post_thread(category=self.category, poster=self.user)
        reported = testutils.post_thread(category=self.category, poster=self.user)

        add_owner(visible, self.user)

        reported.has_reported_posts = True
        reported.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['count'], 1)
        self.assertEqual(response_json['results'][0]['id'], visible.id)

        # threads with reported posts will also show to moderators
        override_acl(self.user, {
            'can_moderate_private_threads': 1
        })

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['count'], 2)
        self.assertEqual(response_json['results'][0]['id'], reported.id)
        self.assertEqual(response_json['results'][1]['id'], visible.id)


class PrivateThreadsListTests(PrivateThreadsApiTestCase):
    def setUp(self):
        super(PrivateThreadsListTests, self).setUp()

        self.test_link = reverse('misago:private-threads')

    def test_unauthenticated(self):
        """view requires user to sign in and be able to access it"""
        self.logout_user()

        response = self.client.get(self.test_link)
        self.assertContains(response, "sign in to use private threads", status_code=403)

    def test_no_permission(self):
        """view requires user to have permission to be able to access it"""
        override_acl(self.user, {
            'can_use_private_threads': 0
        })

        response = self.client.get(self.test_link)
        self.assertContains(response, "use private threads", status_code=403)

    def test_empty_list(self):
        """view has no showstoppers on returning empty list"""
        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "empty-message")

    def test_thread_visibility(self):
        """only participated threads are returned by private threads view"""
        visible = testutils.post_thread(category=self.category, poster=self.user)
        hidden = testutils.post_thread(category=self.category, poster=self.user)
        reported = testutils.post_thread(category=self.category, poster=self.user)

        add_owner(visible, self.user)

        reported.has_reported_posts = True
        reported.save()

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, visible.get_absolute_url())

        # threads with reported posts will also show to moderators
        override_acl(self.user, {
            'can_moderate_private_threads': 1
        })

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reported.get_absolute_url())
        self.assertContains(response, visible.get_absolute_url())
