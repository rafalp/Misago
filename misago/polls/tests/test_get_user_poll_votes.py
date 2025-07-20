from ..votes import get_user_poll_votes


def test_get_user_poll_votes_returns_set_with_user_poll_vote(
    user, poll, poll_vote_factory
):
    choice_id = poll.choices[0]["id"]

    poll_vote_factory(poll, user, choice_id)

    assert get_user_poll_votes(user, poll) == {choice_id}


def test_get_user_poll_votes_returns_set_with_user_poll_votes(
    user, poll, poll_vote_factory
):
    choice_id1 = poll.choices[0]["id"]
    choice_id2 = poll.choices[-1]["id"]

    poll_vote_factory(poll, user, choice_id1)
    poll_vote_factory(poll, user, choice_id2)

    assert get_user_poll_votes(user, poll) == {choice_id1, choice_id2}


def test_get_user_poll_votes_returns_empty_set_if_user_didnt_vote(user, poll):
    assert get_user_poll_votes(user, poll) == set()


def test_get_user_poll_votes_returns_empty_set_if_user_is_anonymous(
    anonymous_user, poll
):
    assert get_user_poll_votes(anonymous_user, poll) == set()
