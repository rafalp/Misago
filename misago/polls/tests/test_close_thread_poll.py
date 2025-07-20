from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..close import close_thread_poll


def test_close_thread_poll_closes_poll(thread, poll, user):
    assert close_thread_poll(thread, poll, user)

    assert poll.is_closed
    assert poll.closed_at
    assert poll.closed_by == user
    assert poll.closed_by_name == user.username
    assert poll.closed_by_slug == user.slug


def test_close_thread_poll_creates_thread_update(thread, poll, user):
    thread_update = close_thread_poll(thread, poll, user)

    assert thread_update
    assert thread_update.action == ThreadUpdateActionName.CLOSED_POLL
    assert thread_update.thread == thread
    assert thread_update.actor == user


def test_close_thread_poll_doesnt_create_thread_update_if_poll_is_already_closed(
    thread, closed_poll, user
):
    assert not close_thread_poll(thread, closed_poll, user)
    assert not ThreadUpdate.objects.exists()
