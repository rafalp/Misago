from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils.six import StringIO

from misago.users.management.commands import deletemarkedusers


UserModel = get_user_model()


class DeleteMArkedUsersTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            'Bob', 'bob@bob.com', 'pass123', delete_own_account=True)

    def test_delete_marked_user(self):
        """deletes marked user"""
        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 1")

        with self.assertRaises(UserModel.DoesNotExist):
            UserModel.objects.get(pk=self.user.pk)

    def test_delete_not_marked(self):
        """user has to be marked to be deletable"""
        self.user.delete_own_account = False
        self.user.save()

        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")
        
        UserModel.objects.get(pk=self.user.pk)

    def test_delete_is_staff(self):
        """staff users are extempt from deletion"""
        self.user.is_staff = True
        self.user.save()

        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")
        
        UserModel.objects.get(pk=self.user.pk)

    def test_delete_superuser(self):
        """superusers are extempt from deletion"""
        self.user.is_superuser = True
        self.user.save()

        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Deleted users: 0")
        
        UserModel.objects.get(pk=self.user.pk)

    @override_settings(MISAGO_ENABLE_DELETE_OWN_ACCOUNT=False)
    def test_delete_disabled(self):
        """deletion is disabled"""
        out = StringIO()
        call_command(deletemarkedusers.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Delete own account option is currently disabled.")
        
        UserModel.objects.get(pk=self.user.pk)