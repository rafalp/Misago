from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from misago.users.management.commands import deleteprofilefield


UserModel = get_user_model()


class DeleteProfileFieldTests(TestCase):
    def test_no_fieldname(self):
        """utility has no showstoppers when no fieldname is given"""
        out = StringIO()
        call_command(deleteprofilefield.Command(), stderr=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Specify fieldname to delete.")

    def test_no_fields_set(self):
        """utility has no showstoppers when no fields are set"""
        out = StringIO()
        call_command(deleteprofilefield.Command(), 'gender', stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, '"gender" profile field has been deleted from 0 users.')

    def test_delete_fields_(self):
        """utility has no showstoppers when no fields are set"""
        user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')
        user.profile_fields = {'gender': 'male', 'bio': "Yup!"}
        user.save()

        out = StringIO()
        call_command(deleteprofilefield.Command(), 'gender', stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, '"gender" profile field has been deleted from 1 users.')

        user = UserModel.objects.get(pk=user.pk)
        self.assertEqual(user.profile_fields, {'bio': "Yup!"})
