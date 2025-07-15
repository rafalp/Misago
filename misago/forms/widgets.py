from django.forms import Textarea, Widget


class ListInput(Widget):
    def value_from_datadict(self, data, files, name):
        return data.getlist(name)


class ListTextarea(Textarea):
    unique: bool

    def __init__(
        self,
        unique: bool = False,
        attrs: dict | None = None,
    ):
        self.unique = unique
        super().__init__(attrs)

    def format_value(self, value):
        if not value:
            return None

        return "\n".join(value)

    def value_from_datadict(self, data, files, name):
        return data.get(name, "").splitlines()


class DictInput(Widget):
    def value_from_datadict(self, data, files, name) -> list[tuple[str, str]]:
        value = []
        for data_key, data_value in data.items():
            if key := self.parse_data_key(data_key, name):
                value.append((key, data_value))
        return value

    def parse_data_key(self, key: str, name: str) -> str | None:
        if not key.startswith(name):
            return None

        key = key[len(name) :]
        if key and key[0] == "[" and key[-1] == "]":
            return key[1:-1] or None
