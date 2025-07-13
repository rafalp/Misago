from math import floor
from typing import TYPE_CHECKING, Iterable, Union

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from .models import Poll, PollVote

if TYPE_CHECKING:
    from ..users.models import User


def get_user_poll_votes(user: Union["User", AnonymousUser], poll: Poll) -> set[str]:
    if user.is_anonymous:
        return set()

    return set(
        PollVote.objects.filter(poll=poll, voter=user).values_list(
            "choice_id", flat=True
        )
    )


def get_poll_results_data(poll: Poll, fetch_voters: bool = False) -> list[dict]:
    remainder = 100
    voted_choices = 0

    data = []
    data_map = {}
    for choice in poll.choices:
        if choice["votes"]:
            share = floor(float(choice["votes"]) * 100 / poll.votes)
            remainder -= share
            voted_choices += 1
        else:
            share = 0

        choice_copy = dict(share=share, voters=[], **choice)
        data.append(choice_copy)
        data_map[choice_copy["id"]] = choice_copy

    if remainder:
        for choice in sorted(data, key=lambda c: c["votes"]):
            if remainder and choice["votes"]:
                choice["share"] += 1
                remainder -= 1

    if fetch_voters:
        queryset = (
            PollVote.objects.filter(poll=poll)
            .values("choice_id", "voter_id", "voter_name", "voter_slug", "voted_at")
            .order_by("id")
        )
        for vote in queryset.iterator():
            data_map[vote["choice_id"]]["voters"].append(
                {
                    "id": vote["voter_id"],
                    "username": vote["voter_name"],
                    "slug": vote["voter_slug"],
                    "voted_at": vote["voted_at"],
                }
            )

    return data


def delete_user_poll_votes(user: "User", poll: Poll, choices: Iterable[str]):
    for choice in poll.choices:
        if choice["id"] in choices:
            choice["votes"] = max(0, choice["votes"] - 1)

    poll.votes = sum(choice["votes"] for choice in poll.choices)

    PollVote.objects.filter(poll=poll, voter=user, choice_id__in=choices).delete()


def save_user_poll_vote(user: "User", poll: Poll, choices: Iterable[str]):
    voted_at = timezone.now()

    PollVote.objects.bulk_create(
        PollVote(
            category_id=poll.category_id,
            thread_id=poll.thread_id,
            poll=poll,
            choice_id=choice_id,
            voter=user,
            voter_name=user.username,
            voter_slug=user.slug,
            voted_at=voted_at,
        )
        for choice_id in choices
    )

    for choice in poll.choices:
        if choice["id"] in choices:
            choice["votes"] += 1

    poll.votes = sum(choice["votes"] for choice in poll.choices)
    poll.save(update_fields=["choices", "votes"])
