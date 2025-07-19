from ..votes import (
    delete_user_poll_votes,
    save_user_poll_vote,
)


def test_delete_user_poll_votes_deletes_user_poll_votes(user, poll):
    choice_id1 = poll.choices[0]["id"]
    choice_id2 = poll.choices[-1]["id"]

    save_user_poll_vote(user, poll, [choice_id1, choice_id2])

    assert [choice["votes"] for choice in poll.choices] == [1, 0, 1]
    assert poll.votes == 2

    delete_user_poll_votes(user, poll, [choice_id1, choice_id2])

    assert [choice["votes"] for choice in poll.choices] == [0, 0, 0]
    assert poll.votes == 0
