from unittest.mock import ANY

from ..models import Poll
from ..votes import get_poll_results_data


def test_get_poll_results_data_calculates_shares():
    poll = Poll(
        choices=[
            {"id": "a", "votes": 1},
            {"id": "b", "votes": 1},
            {"id": "c", "votes": 0},
        ],
        votes=2,
    )
    assert sum(choice["share"] for choice in get_poll_results_data(poll)) == 100


def test_get_poll_results_data_uses_hamilton_remainders_method():
    poll = Poll(
        choices=[
            {"id": "a", "votes": 1},
            {"id": "b", "votes": 1},
            {"id": "c", "votes": 1},
        ],
        votes=3,
    )
    assert sum(choice["share"] for choice in get_poll_results_data(poll)) == 100


def test_get_poll_results_data_handles_poll_without_votes():
    poll = Poll(
        choices=[
            {"id": "a", "votes": 0},
            {"id": "b", "votes": 0},
            {"id": "c", "votes": 0},
        ],
        votes=0,
    )
    assert sum(choice["share"] for choice in get_poll_results_data(poll)) == 0


def test_get_poll_results_data_includes_votes(user_poll, poll_vote_factory):
    for i, choice in enumerate(user_poll.choices, 1):
        poll_vote_factory(user_poll, f"Voter{i}", choice["id"])

    results = get_poll_results_data(user_poll, fetch_voters=True)
    assert results == [
        {
            "id": user_poll.choices[0]["id"],
            "name": user_poll.choices[0]["name"],
            "votes": 1,
            "share": 34,
            "voters": [
                {
                    "id": None,
                    "username": "Voter1",
                    "slug": "voter1",
                    "voted_at": ANY,
                },
            ],
        },
        {
            "id": user_poll.choices[1]["id"],
            "name": user_poll.choices[1]["name"],
            "votes": 1,
            "share": 33,
            "voters": [
                {
                    "id": None,
                    "username": "Voter2",
                    "slug": "voter2",
                    "voted_at": ANY,
                },
            ],
        },
        {
            "id": user_poll.choices[2]["id"],
            "name": user_poll.choices[2]["name"],
            "votes": 1,
            "share": 33,
            "voters": [
                {
                    "id": None,
                    "username": "Voter3",
                    "slug": "voter3",
                    "voted_at": ANY,
                },
            ],
        },
    ]
