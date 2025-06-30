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


def test_poll_choices_with_shares_calculates_shares():
    poll = Poll(choices=[{"votes": 1}, {"votes": 1}, {"votes": 0}], votes=2)
    assert sum(choice["share"] for choice in poll.choices_with_shares) == 100


def test_poll_choices_with_shares_users_hamilton_remainders_method():
    poll = Poll(choices=[{"votes": 1}, {"votes": 1}, {"votes": 1}], votes=3)
    assert sum(choice["share"] for choice in poll.choices_with_shares) == 100
