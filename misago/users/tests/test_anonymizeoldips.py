import datetime

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone
from django.utils.six import StringIO
from django.test import TestCase, override_settings

from misago.core.utils import ANONYMOUS_IP
from misago.users.management.commands import anonymizeoldips


UserModel = get_user_model()


class AnonymizeOldIpsTests(TestCase):
    def test_anonymizeoldips_new_user(self):
        """command is not anonymizing user's IP if its new"""
        user = UserModel.objects.create_user('Bob', 'bob@bob.com')
        call_command(anonymizeoldips.Command())
        user_joined_from_ip = UserModel.objects.get(pk=user.pk).joined_from_ip
        
        self.assertNotEqual(user_joined_from_ip, ANONYMOUS_IP)
    
    def test_anonymizeoldips_old_user(self):
        """command is anonymizing user's IP if its old"""
        current_datetime = timezone.now()
        datetime_50_days_past = current_datetime - datetime.timedelta(days=51)
        user = UserModel.objects.create_user('Bob', 'bob@bob.com')
        user.joined_on = datetime_50_days_past
        user.save()
        call_command(anonymizeoldips.Command())
        user_joined_from_ip = UserModel.objects.get(pk=user.pk).joined_from_ip

        self.assertEqual(user_joined_from_ip, ANONYMOUS_IP)

    @override_settings(MISAGO_IP_STORE_TIME = None)
    def test_not_anonymizing_user_ip(self):
        """command is not anonymizing user's IP if anonymization is disabled"""
        out = StringIO()
        call_command(anonymizeoldips.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "IP anonymization is disabled.")