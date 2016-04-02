import json

from misago.users.testutils import AuthenticatedUserTestCase
from misago.categories.models import Category

from misago.threads import testutils


class ThreadApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')

        self.thread = testutils.post_thread(category=self.category)
        self.api_link = '/api/threads/%s/' % self.thread.pk

    def get_thread_json(self):
        response = self.client.get('/api/threads/%s/' % self.thread.pk)
        self.assertEqual(response.status_code, 200)

        return json.loads(response.content)


class ThreadsReadApiTests(ThreadApiTestCase):
    def setUp(self):
        super(ThreadSubscribeApiTests, self).setUp()
        self.api_link = '/api/threads/read/'

    def read_all_threads(self):
        """api sets all threads as read"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.categoryread_set.count(), 2)

    def read_threads_in_category(self):
        """api sets threads in category as read"""
        response = self.client.post(
            '%s?category=%s' % (self.api_link, self.category.pk))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.categoryread_set.count(), 1)


class ThreadSubscribeApiTests(ThreadApiTestCase):
    def setUp(self):
        super(ThreadSubscribeApiTests, self).setUp()

        self.api_link = '/api/threads/%s/subscribe/' % self.thread.pk

    def test_subscribe_thread(self):
        """api makes it possible to subscribe thread"""
        response = self.client.post(self.api_link, json.dumps({
            'notify': True
        }),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['subscription'])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertFalse(subscription.send_email)

    def test_subscribe_thread_with_email(self):
        """api makes it possible to subscribe thread with emails"""
        response = self.client.post(self.api_link, json.dumps({
            'email': True
        }),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['subscription'])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertTrue(subscription.send_email)

    def test_unsubscribe_thread(self):
        """api makes it possible to unsubscribe thread"""
        response = self.client.post(self.api_link, json.dumps({
            'remove': True
        }),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json['subscription'])

        self.assertEqual(self.user.subscription_set.count(), 0)

    def test_subscribe_as_guest(self):
        """api makes it impossible to subscribe thread"""
        self.logout_user()

        response = self.client.post(self.api_link, json.dumps({
            'notify': True
        }),
        content_type="application/json")

        self.assertEqual(response.status_code, 403)

    def test_subscribe_nonexistant_thread(self):
        """api makes it impossible to subscribe nonexistant thread"""
        bad_api_link = self.api_link.replace(
            unicode(self.thread.pk), unicode(self.thread.pk + 9))
        response = self.client.post(bad_api_link, json.dumps({
            'notify': True
        }),
        content_type="application/json")

        self.assertEqual(response.status_code, 404)
