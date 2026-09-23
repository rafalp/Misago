from ...threadevents.enums import ThreadEventTypeName
from ...threadevents.models import ThreadEvent
from ..close import close_thread_poll


def test_close_thread_poll_closes_poll(thread, poll, user):
    assert close_thread_poll(thread, poll, user)

    assert poll.is_closed
    assert poll.closed_at
    assert poll.closed_by == user
    assert poll.closed_by_name == user.username
    assert poll.closed_by_slug == user.slug


def test_close_thread_poll_creates_thread_event(thread, poll, user):
    thread_event = close_thread_poll(thread, poll, user)

    assert thread_event
    assert thread_event.event_type == ThreadEventTypeName.CLOSED_POLL
    assert thread_event.thread == thread
    assert thread_event.actor == user


def test_close_thread_poll_doesnt_create_thread_event_if_poll_is_already_closed(
    thread, closed_poll, user
):
    assert not close_thread_poll(thread, closed_poll, user)
    assert not ThreadEvent.objects.exists()
