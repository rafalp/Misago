from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from ...conf.test import override_dynamic_settings
from ..management.commands import deletemarkedusers
from ..test import create_test_user

User = get_user_model()


class DeleteMarkedUsersTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")
        self.user.mark_for_delete()

    def test_delete_marked_user(self):
        """deletes marked user"""
        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 1")

        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()

    @override_dynamic_settings(allow_delete_own_account=False)
    def test_delete_disabled(self):
        """deletion respects user decision even if configuration has changed"""
        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 1")

        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()

    def test_delete_not_marked(self):
        """user has to be marked to be deletable"""
        self.user.is_deleting_account = False
        self.user.save()

        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")

        self.user.refresh_from_db()

    def test_delete_is_staff(self):
        """staff users are extempt from deletion"""
        self.user.is_staff = True
        self.user.save()

        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")

        self.user.refresh_from_db()

    def test_delete_superuser(self):
        """superusers are extempt from deletion"""
        self.user.is_superuser = True
        self.user.save()

        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")

        self.user.refresh_from_db()
