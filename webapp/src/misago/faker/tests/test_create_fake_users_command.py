from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command

from ..management.commands import createfakeusers

User = get_user_model()


def test_management_command_creates_fake_users(db):
    call_command(createfakeusers.Command(), stdout=StringIO())
    assert User.objects.exists()
