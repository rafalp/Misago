from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from ..management.commands import listusedprofilefields
from ..test import create_test_user


class ListUsedProfileFieldsTests(TestCase):
    def test_no_fields_set(self):
        """utility has no showstoppers when no fields are set"""
        create_test_user("User", "user@example.com")

        out = StringIO()
        call_command(listusedprofilefields.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "No profile fields are currently in use.")

    def test_fields_set(self):
        """utility lists number of users that have different fields set"""
        create_test_user(
            "User1",
            "user1@example.com",
            profile_fields={"gender": "male", "bio": "Yup!"},
        )
        create_test_user(
            "User2", "user2@example.com", profile_fields={"gender": "male"}
        )
        create_test_user("User3", "user3@example.com", profile_fields={"location": ""})

        out = StringIO()
        call_command(listusedprofilefields.Command(), stdout=out)
        command_output = [l.strip() for l in out.getvalue().strip().splitlines()]

        self.assertEqual(command_output, ["bio:      1", "gender:   2", "location: 1"])
