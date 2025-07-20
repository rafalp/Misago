from django.forms import Textarea, Widget


class DictInput(Widget):
    template_name = None

    def value_from_datadict(self, data, files, name) -> dict[str, str]:
        value = {}
        for data_key, data_value in data.items():
            if key := self.parse_data_key(data_key, name):
                value[key] = data_value
        return value

    def parse_data_key(self, key: str, name: str) -> str | None:
        if not key.startswith(name):
            return None

        key = key[len(name) :]
        if key and key[0] == "[" and key[-1] == "]":
            return key[1:-1] or None

    def format_value(self, value):
        if not value:
            return {}

        return value


class ListInput(Widget):
    template_name = None

    def value_from_datadict(self, data, files, name):
        return [item for item in data.getlist(name) if item.strip()]

    def format_value(self, value):
        if not value:
            return []

        return value


class ListTextarea(Textarea):
    template_name = None

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
        return [line for line in data.get(name, "").splitlines() if line.strip()]
