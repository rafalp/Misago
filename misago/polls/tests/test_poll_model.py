from datetime import timedelta

from django.utils import timezone

from ..models import Poll


def test_poll_ends_at_is_none_for_infinite_poll():
    poll = Poll()
    assert poll.ends_at is None


def test_poll_ends_at_returns_calculated_timestamp():
    poll = Poll(duration=4)
    assert poll.ends_at


def test_poll_has_ended_is_false_for_infinite_poll():
    poll = Poll()
    assert poll.has_ended is False


def test_poll_has_ended_is_false_for_future_end_date():
    poll = Poll(started_at=timezone.now(), duration=4)
    assert poll.has_ended is False


def test_poll_has_ended_is_true_for_passed_end_date():
    poll = Poll(started_at=timezone.now() - timedelta(days=5), duration=4)
    assert poll.has_ended is True
