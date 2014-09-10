from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.users.testutils import UserTestCase, AuthenticatedUserTestCase

from misago.notifications.api import notify_user


class NotificationViewsTests(AuthenticatedUserTestCase):
    def setUp(self):
        self.view_link = reverse('misago:notifications')
        self.ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        super(NotificationViewsTests, self).setUp()

    def notify_user(self):
        notification = notify_user(self.user,
                                   "Test notify %(token)s",
                                   "/users/",
                                   "test",
                                   {'token': 'Bob'},
                                   self.user)
        self.user = get_user_model().objects.get(id=self.user.id)
        return notification

    def test_list(self):
        """get request to list renders list"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("have any notifications", response.content)

        self.notify_user()

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test notify <strong>Bob</strong>", response.content)

    def test_list_ajax(self):
        """get ajax to list renders list"""
        response = self.client.get(self.view_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("have any new notifications", response.content)

        self.notify_user()

        response = self.client.get(self.view_link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test notify <strong>Bob</strong>", response.content)

    def test_read_one(self):
        """read_notification POST reads one notification"""
        self.notify_user()
        notification = self.notify_user()
        self.notify_user()

        response = self.client.post(self.view_link, data={
            'notification': notification.pk,
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.new_notifications, 2)

        notification = self.user.notifications.get(id=notification.pk)
        self.assertFalse(notification.is_new)

    def test_read_one_ajax(self):
        """read_notification ajax POST reads one notification"""
        self.notify_user()
        notification = self.notify_user()
        self.notify_user()

        response = self.client.post(self.view_link, data={
            'notification': notification.pk,
        },**self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.new_notifications, 2)

        notification = self.user.notifications.get(id=notification.pk)
        self.assertFalse(notification.is_new)

    def test_read_all(self):
        """read_all POST request to list sets all notifications as read"""
        self.notify_user()

        response = self.client.post(self.view_link, data={
            'read-all': True,
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.new_notifications, 0)

    def test_read_all_ajax(self):
        """real_all POST ajax to list sets all notifications as read"""
        self.notify_user()

        response = self.client.post(self.view_link, data={
            'read-all': True,
        },**self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.new_notifications, 0)


class AnonymousNotificationsViewsTests(UserTestCase):
    def setUp(self):
        self.view_link = reverse('misago:notifications')
        self.ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        super(AnonymousNotificationsViewsTests, self).setUp()

    def test_get(self):
        """get request to list returns 403 for guests"""
        response = self.client.get(self.view_link)
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        """post request to list returns 403 for guests"""
        response = self.client.post(self.view_link)
        self.assertEqual(response.status_code, 403)

    def test_get_ajax(self):
        """get ajax request to list returns 403 for guests"""
        response = self.client.get(self.view_link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

    def test_post_ajax(self):
        """post ajax request to list returns 403 for guests"""
        response = self.client.post(self.view_link, **self.ajax_header)
        self.assertEqual(response.status_code, 403)

