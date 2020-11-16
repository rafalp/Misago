from io import StringIO

from django.core.management import call_command

from ...threads.models import Thread
from ..management.commands import createfakethreads


def test_management_command_creates_fake_threads(db):
    call_command(createfakethreads.Command(), stdout=StringIO())
    assert Thread.objects.exists()
