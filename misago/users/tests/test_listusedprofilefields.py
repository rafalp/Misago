from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from misago.users.management.commands import listusedprofilefields


User = get_user_model()


class ListUsedProfileFieldsTests(TestCase):
    def test_no_fields_set(self):
        """utility has no showstoppers when no fields are set"""
        User.objects.create_user("Bob", "bob@bob.com", "pass123")

        out = StringIO()
        call_command(listusedprofilefields.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "No profile fields are currently in use.")

    def test_fields_set(self):
        """utility lists number of users that have different fields set"""
        user = User.objects.create_user("Bob", "bob@bob.com", "pass123")
        user.profile_fields = {"gender": "male", "bio": "Yup!"}
        user.save()

        user = User.objects.create_user("Bob2", "bob2@bob.com", "pass123")
        user.profile_fields = {"gender": "male"}
        user.save()

        user = User.objects.create_user("Bob3", "bob3@bob.com", "pass123")
        user.profile_fields = {"location": ""}
        user.save()

        out = StringIO()
        call_command(listusedprofilefields.Command(), stdout=out)
        command_output = [l.strip() for l in out.getvalue().strip().splitlines()]

        self.assertEqual(command_output, ["bio:      1", "gender:   2", "location: 1"])
