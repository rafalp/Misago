from ...threadevents.enums import ThreadUpdateActionName
from ...threadevents.models import ThreadEvent
from ..close import open_thread_poll


def test_open_thread_poll_opens_poll(thread, closed_poll, user):
    assert open_thread_poll(thread, closed_poll, user)

    assert not closed_poll.is_closed
    assert not closed_poll.closed_at
    assert not closed_poll.closed_by
    assert not closed_poll.closed_by_name
    assert not closed_poll.closed_by_slug


def test_open_thread_poll_creates_thread_event(thread, closed_poll, user):
    thread_event = open_thread_poll(thread, closed_poll, user)

    assert thread_event
    assert thread_event.action == ThreadUpdateActionName.OPENED_POLL
    assert thread_event.thread == thread
    assert thread_event.actor == user

    thread.refresh_from_db()
    assert thread.has_events


def test_open_thread_poll_doesnt_create_thread_event_if_poll_is_already_open(
    thread, poll, user
):
    assert not open_thread_poll(thread, poll, user)
    assert not ThreadEvent.objects.exists()
