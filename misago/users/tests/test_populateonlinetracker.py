from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from misago.users.management.commands import populateonlinetracker
from misago.users.models import Online


UserModel = get_user_model()


class PopulateOnlineTrackerTests(TestCase):
    def test_populate_user_online(self):
        """user account without online tracker gets one"""
        test_user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        Online.objects.filter(user=test_user).delete()
        self.assertEqual(Online.objects.filter(user=test_user).count(), 0)

        out = StringIO()
        call_command(populateonlinetracker.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, 'Tracker entries created: 1')
        self.assertEqual(Online.objects.filter(user=test_user).count(), 1)
