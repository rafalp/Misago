from django.forms import Field

from .widgets import ListTextarea


class ListField(Field):
    widget = ListTextarea

    strip: bool
    unique: bool
    lowercase: bool
    uppercase: bool
    case_insensitive: bool

    def __init__(
        self,
        *,
        strip: bool = True,
        unique: bool = False,
        lowercase: bool = False,
        uppercase: bool = False,
        case_insensitive: bool = False,
        **kwargs,
    ):
        if lowercase and uppercase:
            raise ValueError(
                "'lowercase' and 'uppercase' options cannot both be enabled."
            )

        if case_insensitive:
            if lowercase:
                raise ValueError(
                    "'case_insensitive' and 'lowercase' options cannot both be enabled."
                )
            if uppercase:
                raise ValueError(
                    "'case_insensitive' and 'uppercase' options cannot both be enabled."
                )
            if not unique:
                raise ValueError(
                    "'case_insensitive' requires 'unique' option to be enabled."
                )

        self.strip = strip
        self.unique = unique
        self.lowercase = lowercase
        self.uppercase = uppercase
        self.case_insensitive = case_insensitive

        super().__init__(**kwargs)

    def to_python(self, value: list[str]) -> list[str]:
        if self.strip:
            value = self.to_python_strip(value)
        if self.lowercase:
            value = [item.lower() for item in value]
        elif self.uppercase:
            value = [item.upper() for item in value]
        if self.unique:
            if self.case_insensitive:
                value = self.to_python_unique_ci(value)
            else:
                value = self.to_python_unique(value)

        return value

    def to_python_strip(self, value: list[str]) -> list[str]:
        clean_value: list[str] = []
        for item in value:
            if clean_item := item.strip():
                clean_value.append(clean_item)
        return clean_value

    def to_python_unique(self, value: list[str]) -> list[str]:
        clean_value: list[str] = []
        for item in value:
            if item not in clean_value:
                clean_value.append(item)
        return clean_value

    def to_python_unique_ci(self, value: list[str]) -> list[str]:
        unique_values: set[str] = set()
        clean_value: list[str] = []
        for item in value:
            item_ci = item.lower()
            if item_ci not in unique_values:
                clean_value.append(item)
                unique_values.add(item_ci)
        return clean_value
