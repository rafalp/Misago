from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..close import open_thread_poll


def test_open_thread_poll_opens_poll(thread, closed_poll, user):
    assert open_thread_poll(thread, closed_poll, user)

    assert not closed_poll.is_closed
    assert not closed_poll.closed_at
    assert not closed_poll.closed_by
    assert not closed_poll.closed_by_name
    assert not closed_poll.closed_by_slug


def test_open_thread_poll_creates_thread_update(thread, closed_poll, user):
    thread_update = open_thread_poll(thread, closed_poll, user)

    assert thread_update
    assert thread_update.action == ThreadUpdateActionName.OPENED_POLL
    assert thread_update.thread == thread
    assert thread_update.actor == user


def test_open_thread_poll_doesnt_create_thread_update_if_poll_is_already_open(
    thread, poll, user
):
    assert not open_thread_poll(thread, poll, user)
    assert not ThreadUpdate.objects.exists()
