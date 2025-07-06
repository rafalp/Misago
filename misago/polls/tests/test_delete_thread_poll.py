import pytest

from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..delete import delete_thread_poll
from ..models import Poll, PollVote


def test_delete_thread_poll_deletes_poll(thread, poll, user):
    delete_thread_poll(thread, poll, user)

    with pytest.raises(Poll.DoesNotExist):
        poll.refresh_from_db()


def test_delete_thread_poll_updates_thread(thread, poll, user):
    assert thread.has_poll

    delete_thread_poll(thread, poll, user)

    thread.refresh_from_db()
    assert not thread.has_poll


def test_delete_thread_poll_creates_thread_update(thread, poll, user):
    delete_thread_poll(thread, poll, user)

    ThreadUpdate.objects.get(
        thread=thread,
        actor=user,
        action=ThreadUpdateActionName.DELETED_POLL,
    )
