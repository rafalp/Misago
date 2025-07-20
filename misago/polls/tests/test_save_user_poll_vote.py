from ..models import PollVote
from ..votes import save_user_poll_vote


def test_save_user_poll_vote_saves_user_vote(user, poll):
    choice_id = poll.choices[0]["id"]

    save_user_poll_vote(user, poll, [choice_id])

    vote = PollVote.objects.get()

    assert vote.category == poll.category
    assert vote.thread == poll.thread
    assert vote.poll == poll
    assert vote.choice_id == choice_id
    assert vote.voter == user
    assert vote.voter_name == user.username
    assert vote.voter_slug == user.slug

    poll.refresh_from_db()
    assert [choice["votes"] for choice in poll.choices] == [1, 0, 0]
    assert poll.votes == 1


def test_save_user_poll_vote_saves_multiple_user_votes(user, poll):
    choice_id1 = poll.choices[0]["id"]
    choice_id2 = poll.choices[-1]["id"]

    save_user_poll_vote(user, poll, [choice_id1, choice_id2])

    PollVote.objects.get(choice_id=choice_id1)
    PollVote.objects.get(choice_id=choice_id2)

    poll.refresh_from_db()
    assert [choice["votes"] for choice in poll.choices] == [1, 0, 1]
    assert poll.votes == 2
