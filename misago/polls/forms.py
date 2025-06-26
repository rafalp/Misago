from django.forms import Field, Widget

from .choices import PollChoice, PollChoices


class PollChoicesWidget(Widget):
    def value_from_datadict(self, data, files, name):
        name_length = len(name)
        ids: set[str] = set()
        value = []

        for key in data:
            key_length = len(key)

            if name_length >= key_length:
                continue

            if key[:name_length] != name:
                continue

            if key[name_length] != "[":
                continue

            if key[key_length - 1] != "]":
                continue

            choice_id = key[name_length + 1 : key_length - 1].strip()
            if not choice_id:
                continue

            if choice_id in ids:
                continue

            if choice := data.get(key, "").strip():
                ids.add(choice_id)
                value.append({"id": choice_id, "name": choice})

        obj = PollChoices(value)

        for choice in data.getlist(f"{name}[]"):
            if choice := choice.strip():
                obj.add(choice)

        return obj

    def check_data_value_name(self, name: str, data_name: str) -> bool:
        if data_name == f"{name}[]":
            return True

        return False


class PollChoicesField(Field):
    widget = PollChoicesWidget

    max_choices: int | None

    def __init__(self, max_choices: int | None = None, **kwargs):
        self.max_choices = max_choices
        super().__init__(**kwargs)

    def clean(self, value) -> PollChoices:
        initial_ids: set[str] = set()
        initial_choices: PollChoice = []

        if self.initial:
            for choice in self.initial.values():
                if choice["id"]:
                    initial_ids.add(choice["id"])
                    initial_choices.append(choice)

        choices = PollChoices(initial_choices)
        for choice in value.get_list():
            if choice["id"] in initial_ids:
                choices[choice["id"]]["name"] = choice["name"]
                initial_ids.remove(choice["id"])
            else:
                choices.add(choice["name"])

        for removed_choice in initial_ids:
            del choices[removed_choice]

        return choices
