from typing import TYPE_CHECKING, Iterable

from django.utils import timezone

from .models import Poll, PollVote

if TYPE_CHECKING:
    from ..users.models import User


def get_user_poll_votes(user: "User", poll: Poll) -> set[str]:
    return set(
        PollVote.objects.filter(poll=poll, voter=user).values_list(
            "choice_id", flat=True
        )
    )


def delete_user_poll_votes(user: "User", poll: Poll, choices: Iterable[str]):
    for choice in poll.choices:
        if choice["id"] in choices:
            choice["votes"] = min(0, choice["votes"] - 1)

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
