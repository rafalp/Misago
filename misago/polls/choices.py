from typing import TypedDict, Iterable

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
    def get_unique_choice_id(cls, ids: Iterable[str]) -> str:
        choice_id = cls.get_random_choice_id()
        while choice_id in ids:
            choice_id = cls.get_random_choice_id()
        return choice_id

    @classmethod
    def get_random_choice_id(cls) -> str:
        return get_random_string(12)

    @classmethod
    def from_str(cls, choices: str) -> "PollChoices":
        obj = cls()

        for name in choices.splitlines():
            if name := name.strip():
                obj.add(name)

        return obj

    def add(self, name: str):
        choice_id = self.get_unique_choice_id(self.choices)

        self.choices[f"_{choice_id}"] = {
            "id": "",
            "name": name,
            "votes": 0,
        }

    def ids(self) -> list[str]:
        return [choice["id"] for choice in self.choices.values() if choice["id"]]

    def names(self) -> list[str]:
        return [choice["name"] for choice in self.choices.values()]

    def values(self) -> list[PollChoice]:
        return list(self.choices.values())

    def inputvalue(self) -> str:
        return "\n".join(self.names())

    def json(self) -> list[PollChoice]:
        ids: set[str] = set(self.ids())

        json: list[PollChoice] = []
        for choice in self.choices.values():
            choice_id = choice.get("id")
            if not choice_id:
                choice_id = self.get_unique_choice_id(ids)

            json.append(
                {
                    "id": choice_id,
                    "name": choice["name"],
                    "votes": choice.get("votes") or 0,
                }
            )

        return json
