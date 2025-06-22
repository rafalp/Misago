from typing import Iterable, Sequence, TypedDict

from django.utils.crypto import get_random_string


class PollChoice(TypedDict):
    id: str
    name: str
    votes: int


class PollChoices:
    choices: dict[str, PollChoice]

    def __init__(self, choices: list[PollChoice]):
        self.choices = {choice["id"]: choice for choice in choices}

    @classmethod
    def from_sequence(cls, choices: Sequence[str]) -> "PollChoices":
        ids: set[str] = set()

        new_choices: list[PollChoice] = []
        for name in choices:
            choice_id = get_random_string(12)
            while choice_id in ids:
                choice_id = get_random_string(12)

            new_choices.append(
                {
                    "id": choice_id,
                    "name": name,
                    "votes": 0,
                }
            )

            ids.add(choice_id)

        return cls(new_choices)

    def to_json(self) -> list[PollChoice]:
        return list(self.choices.values())
