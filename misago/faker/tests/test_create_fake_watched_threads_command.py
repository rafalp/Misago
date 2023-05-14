from io import StringIO

from django.core.management import call_command

from ...notifications.models import WatchedThread
from ..management.commands import createfakewatchedthreads


def test_management_command_creates_watched_threads(
    user, other_user, thread, other_thread
):
    call_command(createfakewatchedthreads.Command(), stdout=StringIO())
    assert WatchedThread.objects.count() == 4  # 2 users x 2 threads
