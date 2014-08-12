from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase

from misago.notifications.api import notify_user


class NotificationViewsTestCase(AdminTestCase):
    def setUp(self):
        self.view_link = reverse('misago:notifications')
        self.ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        super(NotificationViewsTestCase, self).setUp()

    def reload_test_admin(self):
        self.test_admin = get_user_model().objects.get(id=self.test_admin.id)

    def notify_user(self):
        notify_user(self.test_admin,
                    "Test notify %(token)s",
                    "/users/",
                    "test",
                    {'token': 'Bob'},
                    self.test_admin)
        self.test_admin = get_user_model().objects.get(id=self.test_admin.id)

    def test_get(self):
        """get request to list renders list"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("have any notifications", response.content)

        self.notify_user()

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test notify <strong>Bob</strong>", response.content)

    def test_post(self):
        """post request to list sets all notifications as read"""
        self.notify_user()

        response = self.client.post(self.view_link)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)

        self.reload_test_admin()
        self.assertEqual(self.test_admin.new_notifications, 0)

    def test_get_ajax(self):
        """get request to list renders list"""
        response = self.client.get(self.view_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("have any notifications", response.content)

        self.notify_user()

        response = self.client.get(self.view_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test notify <strong>Bob</strong>", response.content)

    def test_post_ajax(self):
        """post request to list sets all notifications as read"""
        self.notify_user()

        response = self.client.post(self.view_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)

        self.reload_test_admin()
        self.assertEqual(self.test_admin.new_notifications, 0)
