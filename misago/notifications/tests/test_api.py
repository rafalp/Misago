from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.notifications import api


class NotificationsAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create_user('Bob', 'bob@bob.com',
                                                  'Pass.123')

    def reload_test_user(self):
        self.test_user = get_user_model().objects.get(id=self.test_user.id)

    def test_notify_user(self):
        """notify_user sets new notification on user"""
        notification = api.notify_user(self.test_user,
                        "Test notify %(token)s",
                        "/users/",
                        "test",
                        {'token': 'Bob'},
                        self.test_user)
        self.assertTrue(notification.is_valid)

        self.reload_test_user()
        self.assertEqual(self.test_user.new_notifications, 1)

    def test_read_user_notification(self):
        """read_user_notification reads user notification"""
        api.notify_user(self.test_user,
                        "Test notify %(token)s",
                        "/users/",
                        "test",
                        {'token': 'Bob'},
                        self.test_user)
        self.reload_test_user()

        api.read_user_notification(self.test_user, "test")

        self.assertEqual(self.test_user.new_notifications, 0)
        queryset = self.test_user.misago_notifications.filter(is_new=True)
        self.assertEqual(queryset.count(), 0)

    def test_read_all_user_alerts(self):
        """read_all_user_alerts marks user notifications as read"""
        api.notify_user(self.test_user,
                        "Test notify %(token)s",
                        "/users/",
                        "test",
                        {'token': 'Bob'},
                        self.test_user)
        self.reload_test_user()

        api.read_all_user_alerts(self.test_user)
        self.assertEqual(self.test_user.new_notifications, 0)

        queryset = self.test_user.misago_notifications.filter(is_new=True)
        self.assertEqual(queryset.count(), 0)

    def test_assert_real_new_notifications_count(self):
        """assert_real_new_notifications_count syncs user notifications"""
        api.notify_user(self.test_user,
                        "Test notify %(token)s",
                        "/users/",
                        "test",
                        {'token': 'Bob'},
                        self.test_user)
        self.reload_test_user()
        api.read_all_user_alerts(self.test_user)

        self.test_user.new_notifications = 42
        self.test_user.save()

        self.reload_test_user()
        self.assertEqual(self.test_user.new_notifications, 42)

        queryset = self.test_user.misago_notifications.filter(is_new=True)
        self.assertEqual(queryset.count(), 0)

        api.assert_real_new_notifications_count(self.test_user)
        self.reload_test_user()
        self.assertEqual(self.test_user.new_notifications, 0)
