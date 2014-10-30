from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from misago.users import bans
from misago.users.management.commands import bansmaintenance
from misago.users.models import Ban, BanCache


class BansMaintenanceTests(TestCase):
    def test_expired_bans_handling(self):
        """expired bans are flagged as such"""
        # create 5 bans then update their valid date to past one
        for i in xrange(5):
            Ban.objects.create(banned_value="abcd")
        bans_expired = (timezone.now() - timedelta(days=10)).date()
        Ban.objects.all().update(valid_until=bans_expired, is_valid=True)

        self.assertEqual(Ban.objects.filter(is_valid=True).count(), 5)

        command = bansmaintenance.Command()

        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, 'Bans invalidated: 5')

        self.assertEqual(Ban.objects.filter(is_valid=True).count(), 0)

    def test_bans_caches_updates(self):
        """ban caches are updated"""
        # create user
        User = get_user_model()
        user = User.objects.create_user("Bob", "bob@boberson.com", "Pass.123")

        # ban user
        Ban.objects.create(banned_value="bob")
        user_ban = bans.get_user_ban(user)

        self.assertIsNotNone(user_ban)
        self.assertEqual(Ban.objects.filter(is_valid=True).count(), 1)

        # first call didn't touch ban
        command = bansmaintenance.Command()

        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue().splitlines()[1].strip()

        self.assertEqual(command_output, 'Ban caches emptied: 0')
        self.assertEqual(Ban.objects.filter(is_valid=True).count(), 1)

        # expire bans
        bans_expired = (timezone.now() - timedelta(days=10)).date()
        Ban.objects.all().update(valid_until=bans_expired, is_valid=True)
        BanCache.objects.all().update(valid_until=bans_expired)

        # invalidate expired ban cache
        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue().splitlines()[1].strip()

        self.assertEqual(command_output, 'Ban caches emptied: 1')
        self.assertEqual(Ban.objects.filter(is_valid=True).count(), 0)

        # see if user is banned anymore
        user = User.objects.get(id=user.id)
        self.assertIsNone(bans.get_user_ban(user))
