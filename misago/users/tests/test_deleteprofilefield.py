from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from ..management.commands import deleteprofilefield
from ..test import create_test_user


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
        call_command(deleteprofilefield.Command(), "gender", stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(
            command_output, '"gender" profile field has been deleted from 0 users.'
        )

    def test_delete_fields(self):
        """utility has no showstoppers when no fields are set"""
        user = create_test_user(
            "User", "user@example.com", profile_fields={"gender": "male", "bio": "Yup!"}
        )

        out = StringIO()
        call_command(deleteprofilefield.Command(), "gender", stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(
            command_output, '"gender" profile field has been deleted from 1 users.'
        )

        user.refresh_from_db()
        self.assertEqual(user.profile_fields, {"bio": "Yup!"})
