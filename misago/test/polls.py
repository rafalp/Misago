from datetime import datetime, timedelta
from typing import Sequence

import pytest
from django.utils import timezone

from ..polls.models import Poll, PollVote
from ..threads.models import Thread
from ..users.models import User
from .utils import (
    FactoryTimestampArg,
    FactoryUserArg,
    factory_timestamp_arg,
    unpack_factory_user_arg,
)


CHOICES = (
    "Yes",
    "No",
    "Maybe",
    "I don't know",
    "Can you repeat the question",
)


@pytest.fixture
def poll_factory():
    def _poll_factory(
        thread: Thread,
        *,
        starter: FactoryUserArg = "PollStarter",
        started_at: FactoryTimestampArg = True,
        closed_at: FactoryTimestampArg = None,
        question: str = "Do you like cookies?",
        choices: Sequence[str] | int = 3,
        duration: int = 5,
        max_choices: int = 1,
        can_change_vote: bool = False,
        is_public: bool = False,
        is_closed: bool = False,
        votes: int = 0,
        closed_by: FactoryUserArg = None,
        update_thread: bool = True,
    ):
        starter_obj, starter_name, starter_slug = unpack_factory_user_arg(starter)
        closed_by_obj, closed_by_name, closed_by_slug = unpack_factory_user_arg(
            closed_by
        )

        if isinstance(choices, int):
            choices_list = CHOICES[:choices]
        else:
            choices_list = choices

        choices_json = []
        for i, choice in enumerate(choices_list):
            choices_json.append({"id": f"choice{i + 1}", "name": choice, "votes": 0})

        if update_thread:
            thread.has_poll = True
            thread.save(update_fields=["has_poll"])

        return Poll.objects.create(
            category_id=thread.category_id,
            thread=thread,
            starter=starter_obj,
            starter_name=starter_name,
            starter_slug=starter_slug,
            started_at=factory_timestamp_arg(started_at),
            closed_at=factory_timestamp_arg(closed_at),
            question=question,
            choices=choices_json,
            duration=duration,
            max_choices=max_choices,
            can_change_vote=can_change_vote,
            is_public=is_public,
            is_closed=is_closed,
            votes=votes,
            closed_by=closed_by_obj,
            closed_by_name=closed_by_name,
            closed_by_slug=closed_by_slug,
        )

    return _poll_factory


@pytest.fixture
def poll(thread, poll_factory):
    return poll_factory(thread)


@pytest.fixture
def ended_poll(user_thread, poll_factory, day_seconds):
    return poll_factory(
        user_thread,
        started_at=day_seconds * -7,
    )


@pytest.fixture
def closed_poll(user_thread, poll_factory):
    return poll_factory(
        user_thread,
        closed_at=True,
        is_closed=True,
        closed_by="Closer",
    )


@pytest.fixture
def user_poll(user, user_thread, poll_factory):
    return poll_factory(user_thread, starter=user)


@pytest.fixture
def ended_user_poll(user, user_thread, poll_factory, day_seconds):
    return poll_factory(
        user_thread,
        starter=user,
        started_at=day_seconds * -7,
    )


@pytest.fixture
def closed_user_poll(user, user_thread, poll_factory):
    return poll_factory(
        user_thread,
        starter=user,
        closed_at=True,
        is_closed=True,
        closed_by="Closer",
    )
