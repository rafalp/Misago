from typing import TypedDict


class PollChoice(TypedDict):
    id: str
    name: str
    votes: int


PollChoices = list[PollChoice]
