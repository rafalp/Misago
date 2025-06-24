from copy import deepcopy
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

    def __getitem__(self, key) -> PollChoice:
        return self.choices[key]

    def __delitem__(self, key):
        del self.choices[key]

    def __contains__(self, key) -> bool:
        return key in self.choices

    @classmethod
    def get_random_choice_id(self) -> str:
        return get_random_string(12)

    @classmethod
    def from_str(cls, choices: str) -> "PollChoices":
        ids: set[str] = set()
        names: set[str] = set()

        new_choices: list[PollChoice] = []
        for name in choices.splitlines():
            name = name.strip()
            if not name or name in names:
                continue

            while not choice_id or choice_id in ids:
                choice_id = cls.get_random_choice_id()

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

    def add_new_choice(self, name: str):
        choice_id = self.get_random_choice_id()
        while choice_id in self.choices:
            choice_id = self.get_random_choice_id()

        self.choices[f"_{choice_id}"] = {
            "id": "",
            "name": name,
            "votes": 0,
        }

    def get_names(self) -> list[str]:
        return [choice["name"] for choice in self.choices.values()]

    def get_str(self) -> str:
        return "\n".join(self.get_names())

    def get_list(self) -> list[PollChoice]:
        return list(self.choices.values())

    def get_json(self) -> list[PollChoice]:
        json: list[PollChoice] = []
        for choice in self.choices.values():
            json.append(
                {
                    "id": choice.get("id") or self.get_random_choice_id(),
                    "name": choice["name"],
                    "votes": choice.get("votes") or 0,
                }
            )

        return json
