from io import StringIO

from django.core.management import call_command

from ..management.commands import populateonlinetracker
from ..models import Online


def test_management_command_creates_online_tracker_for_user_without_one(user):
    Online.objects.filter(user=user).delete()
    assert not Online.objects.filter(user=user).exists()

    call_command(populateonlinetracker.Command(), stdout=StringIO())
    assert Online.objects.filter(user=user).exists()


def test_management_command_displays_message_with_number_of_created_trackers(user):
    Online.objects.filter(user=user).delete()
    assert not Online.objects.filter(user=user).exists()

    out = StringIO()
    call_command(populateonlinetracker.Command(), stdout=out)
    command_output = out.getvalue().splitlines()[0].strip()
    assert command_output == "Tracker entries created: 1"
