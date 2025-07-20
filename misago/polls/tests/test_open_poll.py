from ..close import open_poll


def test_open_poll_closes_poll(user, closed_poll):
    assert open_poll(closed_poll, user)

    assert not closed_poll.is_closed
    assert not closed_poll.closed_at
    assert not closed_poll.closed_by
    assert not closed_poll.closed_by_name
    assert not closed_poll.closed_by_slug

    closed_poll.refresh_from_db()

    assert not closed_poll.is_closed
    assert not closed_poll.closed_at
    assert not closed_poll.closed_by
    assert not closed_poll.closed_by_name
    assert not closed_poll.closed_by_slug


def test_open_poll_returns_false_if_poll_is_already_open(user, poll):
    assert not open_poll(poll, user)

    assert not poll.is_closed
    assert not poll.closed_at
    assert not poll.closed_by
    assert not poll.closed_by_name
    assert not poll.closed_by_slug
