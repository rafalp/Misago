from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone
from django.utils.six import StringIO

from misago.core.utils import ANONYMOUS_IP
from misago.users.management.commands import removeoldips


UserModel = get_user_model()


class RemoveOldIpsTests(TestCase):
    def test_removeoldips_recent_user(self):
        """command is not anonymizing user's IP if its recent"""
        user = UserModel.objects.create_user('Bob', 'bob@bob.com')
        call_command(removeoldips.Command())
        user_joined_from_ip = UserModel.objects.get(pk=user.pk).joined_from_ip
        
        self.assertNotEqual(user_joined_from_ip, ANONYMOUS_IP)
    
    def test_removeoldips_old_user(self):
        """command is anonymizing user's IP if its old"""
        joined_on_past = timezone.now() - timedelta(days=50)
        user = UserModel.objects.create_user('Bob1', 'bob1@bob.com')
        user.joined_on = joined_on_past
        user.save()

        call_command(removeoldips.Command())
        user_joined_from_ip = UserModel.objects.get(pk=user.pk).joined_from_ip
        self.assertEqual(user_joined_from_ip, ANONYMOUS_IP)

    @override_settings(MISAGO_IP_STORE_TIME=None)
    def test_not_anonymizing_user_ip(self):
        """command is not anonymizing user's IP if anonymization is disabled"""
        user = UserModel.objects.create_user('Bob1', 'bob1@bob.com')
        
        out = StringIO()
        call_command(removeoldips.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()
        
        self.assertEqual(command_output, "IP anonymization is disabled.")
        
        user_joined_from_ip = UserModel.objects.get(pk=user.pk).joined_from_ip
        self.assertNotEqual(user_joined_from_ip, ANONYMOUS_IP)

