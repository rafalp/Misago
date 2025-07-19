import pytest

from ..delete import delete_poll
from ..models import Poll, PollVote


def test_delete_poll_deletes_poll(poll):
    delete_poll(poll)

    with pytest.raises(Poll.DoesNotExist):
        poll.refresh_from_db()


def test_delete_poll_deletes_poll_votes(poll):
    poll_vote = PollVote.objects.create(
        category=poll.category,
        thread=poll.thread,
        poll=poll,
        choice_id="asdfghjkl123",
        voter_name="Voter",
        voter_slug="voter",
    )

    delete_poll(poll)

    with pytest.raises(PollVote.DoesNotExist):
        poll_vote.refresh_from_db()
