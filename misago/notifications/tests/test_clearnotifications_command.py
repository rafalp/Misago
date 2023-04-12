from datetime import timedelta
from io import StringIO

from django.core import management
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..management.commands import clearnotifications
from ..models import Notification


def call_command():
    command = clearnotifications.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return out.getvalue().strip().splitlines()[-1].strip()


def test_command_works_if_there_are_no_notifications(db):
    command_output = call_command()
    assert command_output == "No old notifications have been deleted."


@override_dynamic_settings(delete_notifications_older_than=5)
def test_recent_notification_is_kept(user, post):
    Notification.objects.create(user=user, verb="TEST")

    command_output = call_command()
    assert command_output == "No old notifications have been deleted."
    assert Notification.objects.exists()


@override_dynamic_settings(delete_notifications_older_than=5)
def test_old_notification_is_deleted(user, post):
    Notification.objects.create(user=user, verb="TEST")
    Notification.objects.update(created_at=timezone.now() - timedelta(days=10))

    command_output = call_command()
    assert command_output == "Deleted 1 old notifications."
    assert not Notification.objects.exists()
