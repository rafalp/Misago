from ..close import close_poll


def test_close_poll_closes_poll(user, poll):
    assert close_poll(poll, user)

    assert poll.is_closed
    assert poll.closed_at
    assert poll.closed_by == user
    assert poll.closed_by_name == user.username
    assert poll.closed_by_slug == user.slug

    poll.refresh_from_db()

    assert poll.is_closed
    assert poll.closed_at
    assert poll.closed_by == user
    assert poll.closed_by_name == user.username
    assert poll.closed_by_slug == user.slug


def test_close_poll_returns_false_if_poll_is_already_closed(user, closed_poll):
    assert not close_poll(closed_poll, user)

    assert closed_poll.is_closed
    assert closed_poll.closed_at
    assert closed_poll.closed_by
    assert closed_poll.closed_by_name
    assert closed_poll.closed_by_slug
