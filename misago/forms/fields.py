from django.forms import Field, ValidationError

from .widgets import DictInput, ListTextarea


class ListField(Field):
    widget = ListTextarea

    strip: bool
    unique: bool
    lowercase: bool
    uppercase: bool
    case_insensitive: bool
    field: Field | None

    def __init__(
        self,
        *,
        strip: bool = True,
        unique: bool = False,
        lowercase: bool = False,
        uppercase: bool = False,
        case_insensitive: bool = False,
        field: Field | None = None,
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

        self.field = field

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

    def clean(self, value: list[str]) -> list:
        if not self.field:
            return value

        clean_data = []
        errors: list[ValidationError | str] = []

        for item in value:
            try:
                item = self.field.to_python(item)
                if item is not None:
                    clean_item = self.field.clean(item)
                    if clean_item is not None:
                        clean_data.append(clean_item)
            except ValidationError as e:
                errors.extend(m for m in e.error_list if m not in errors)

        if errors:
            raise ValidationError(errors)

        return clean_data

    def validate(self, value: list):
        pass


class DictField(Field):
    def __init__(
        self,
        *,
        key_field: Field | None = None,
        value_field: Field | None = None,
        **kwargs,
    ):
        self.key_field = key_field
        self.value_field = value_field
