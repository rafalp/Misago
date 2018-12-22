from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from misago.users.management.commands import removeoldips


User = get_user_model()

USER_IP = "31.41.51.65"


class RemoveOldIpsTests(TestCase):
    def test_removeoldips_recent_user(self):
        """command is not removing user's IP if its recent"""
        user = User.objects.create_user("Bob", "bob@bob.com", joined_from_ip=USER_IP)

        out = StringIO()
        call_command(removeoldips.Command(), stdout=out)

        user_joined_from_ip = User.objects.get(pk=user.pk).joined_from_ip
        self.assertEqual(user_joined_from_ip, USER_IP)

    def test_removeoldips_old_user(self):
        """command removes user's IP if its old"""
        joined_on_past = timezone.now() - timedelta(days=50)
        user = User.objects.create_user("Bob1", "bob1@bob.com", joined_from_ip=USER_IP)
        user.joined_on = joined_on_past
        user.save()

        out = StringIO()
        call_command(removeoldips.Command(), stdout=out)

        user_joined_from_ip = User.objects.get(pk=user.pk).joined_from_ip
        self.assertIsNone(user_joined_from_ip)

    @override_settings(MISAGO_IP_STORE_TIME=None)
    def test_not_removing_user_ip(self):
        """command is not removing user's IP if removing is disabled"""
        user = User.objects.create_user("Bob1", "bob1@bob.com", joined_from_ip=USER_IP)

        out = StringIO()
        call_command(removeoldips.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Old IP removal is disabled.")

        user_joined_from_ip = User.objects.get(pk=user.pk).joined_from_ip
        self.assertEqual(user_joined_from_ip, USER_IP)
