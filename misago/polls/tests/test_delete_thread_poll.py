import pytest

from ...threadevents.enums import ThreadEventActionName
from ..delete import delete_thread_poll
from ..models import Poll


def test_delete_thread_poll_deletes_poll(thread, poll, user):
    delete_thread_poll(thread, poll, user)

    with pytest.raises(Poll.DoesNotExist):
        poll.refresh_from_db()


def test_delete_thread_poll_updates_thread(thread, poll, user):
    assert thread.has_poll

    delete_thread_poll(thread, poll, user)

    thread.refresh_from_db()
    assert not thread.has_poll


def test_delete_thread_poll_creates_thread_event(thread, poll, user):
    thread_event = delete_thread_poll(thread, poll, user)

    assert thread_event
    assert thread_event.action == ThreadEventActionName.DELETED_POLL
    assert thread_event.thread == thread
    assert thread_event.actor == user

    thread.refresh_from_db()
    assert thread.has_events
