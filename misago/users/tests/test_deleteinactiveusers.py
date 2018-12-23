from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from misago.users.management.commands import deleteinactiveusers
from misago.users.test import create_test_user

User = get_user_model()


class DeleteInactiveUsersTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")

    @override_settings(MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS=2)
    def test_delete_user_activation_user(self):
        """deletes user that didn't activate their account within required time"""
        self.user.joined_on = timezone.now() - timedelta(days=2)
        self.user.requires_activation = User.ACTIVATION_USER
        self.user.save()

        out = StringIO()
        call_command(deleteinactiveusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 1")

        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()

    @override_settings(MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS=2)
    def test_delete_user_activation_admin(self):
        """deletes user that wasn't activated by admin within required time"""
        self.user.joined_on = timezone.now() - timedelta(days=2)
        self.user.requires_activation = User.ACTIVATION_ADMIN
        self.user.save()

        out = StringIO()
        call_command(deleteinactiveusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 1")

        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()

    @override_settings(MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS=2)
    def test_skip_new_user_activation_user(self):
        """skips inactive user that is too new"""
        self.user.joined_on = timezone.now() - timedelta(days=1)
        self.user.requires_activation = User.ACTIVATION_USER
        self.user.save()

        out = StringIO()
        call_command(deleteinactiveusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")

        self.user.refresh_from_db()

    @override_settings(MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS=2)
    def test_skip_new_user_activation_admin(self):
        """skips admin-activated user that is too new"""
        self.user.joined_on = timezone.now() - timedelta(days=1)
        self.user.requires_activation = User.ACTIVATION_ADMIN
        self.user.save()

        out = StringIO()
        call_command(deleteinactiveusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")

        self.user.refresh_from_db()

    @override_settings(MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS=2)
    def test_skip_active_user(self):
        """skips active user"""
        self.user.joined_on = timezone.now() - timedelta(days=1)
        self.user.save()

        out = StringIO()
        call_command(deleteinactiveusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")

        self.user.refresh_from_db()

    @override_settings(MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS=0)
    def test_delete_inactive_is_disabled(self):
        """skips active user"""
        self.user.joined_on = timezone.now() - timedelta(days=1)
        self.user.requires_activation = User.ACTIVATION_ADMIN
        self.user.save()

        out = StringIO()
        call_command(deleteinactiveusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(
            command_output,
            "Automatic deletion of inactive users is currently disabled.",
        )

        self.user.refresh_from_db()
