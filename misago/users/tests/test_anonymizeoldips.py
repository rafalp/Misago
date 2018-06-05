import datetime
import pytz

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.utils import timezone

from misago.conf import settings
from misago.users.management.commands import anonymizeoldips
from misago.core.utils import ANONYMOUS_IP


# - command is not anonymizing user's IP if anonymization is disabled
# - command is anonymizing user's IP if its old

UserModel = get_user_model()


class AnonymizeOldIpsTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')
        self.user_with_joined_on = UserModel.objects.create_user('Bob1', 'bob1@bob.com', 'pass1231')
        self.user_with_joined_on.joined_on = datetime.datetime(2013, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
        self.user_with_joined_on.save()

    def test_anonymizeoldips_new_user(self):
        """ command is not anonymizing user's IP if its new """

        call_command(anonymizeoldips.Command())
        user_joined_from_ip = UserModel.objects.get(pk=self.user.pk).joined_from_ip

        self.assertFalse(user_joined_from_ip == ANONYMOUS_IP, msg=None)
    
    def test_anonymizeoldips_old_user(self):
        """ command is anonymizing user's IP if its old """
        call_command(anonymizeoldips.Command())

        user_with_joined_on = UserModel.objects.get(pk=self.user_with_joined_on.pk)
        timediff = datetime.datetime.now(timezone.utc) - user_with_joined_on.joined_on

        self.assertTrue(timediff.days > settings.MISAGO_IP_STORE_TIME, msg=None)
