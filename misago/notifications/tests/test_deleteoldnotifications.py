from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from misago.notifications import notify_user
from misago.notifications.management.commands import deleteoldnotifications


class DeleteOldNotificatinsTests(TestCase):
    def test_regen_blank_avatar(self):
        """command deletes old notifications"""
        # create user
        User = get_user_model()
        user = User.objects.create_user("Bob", "bob@boberson.com", "Pass.123")

        # notify him
        notify_user(user, "Hello Bob!", "/")

        # run command
        command = deleteoldnotifications.Command()

        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, 'Old notifications have been deleted')
        self.assertEqual(user.misago_notifications.count(), 1)

        # outdate notifications
        cutoff = timedelta(days=settings.MISAGO_NOTIFICATIONS_MAX_AGE * 2)
        cutoff_date = timezone.now() - cutoff

        user.misago_notifications.update(date=cutoff_date)

        # run command again
        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, 'Old notifications have been deleted')
        self.assertEqual(user.misago_notifications.count(), 0)
