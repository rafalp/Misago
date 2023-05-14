from io import StringIO

from django.core.management import call_command

from ...notifications.models import Notification
from ..management.commands import createfakenotifications


def test_management_command_creates_notifications(
    user, other_user, thread, reply, other_thread
):
    call_command(createfakenotifications.Command(), stdout=StringIO())
    assert Notification.objects.count() == 6  # 2 users x 3 posts
