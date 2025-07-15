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
