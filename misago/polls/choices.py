from typing import TypedDict

from django.utils.crypto import get_random_string


class PollChoice(TypedDict):
    id: str
    name: str
    votes: int


class PollChoices:
    choices: dict[str, PollChoice]

    def __init__(self, choices: list[PollChoice] | None = None):
        self.choices = {}

        if choices:
            self.choices = {choice["id"]: choice for choice in choices}

    def __bool__(self) -> bool:
        return bool(self.choices)

    def __len__(self) -> int:
        return len(self.choices)

    @classmethod
    def from_str(cls, choices: str) -> "PollChoices":
        ids: set[str] = set()
        names: set[str] = set()

        new_choices: list[PollChoice] = []
        for name in choices.splitlines():
            name = name.strip()
            if not name or name in names:
                continue

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
            names.add(name)

        return cls(new_choices)

    def get_names(self) -> list[str]:
        return [choice["name"] for choice in self.choices.values()]

    def get_str(self) -> str:
        return "\n".join(self.get_names())

    def get_json(self) -> list[PollChoice]:
        return list(self.choices.values())
