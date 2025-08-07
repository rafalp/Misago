import copy
from typing import Any, Callable, Iterable

from django.forms import Field, ValidationError
from django.utils.translation import pgettext_lazy as _

from .widgets import DictInput, ListTextarea


class DictField(Field):
    widget = DictInput
    default_error_messages = {
        "invalid_choice": _(
            "dict field error",
            "Select a valid choice. %(value)s is not one of the available choices.",
        ),
        "invalid_dict": _("dict field error", "Enter a dict."),
        "invalid_key": _("dict field error", "Key ."),
    }

    coerce: Callable
    strip: bool
    key_field: Field | None
    value_field: Field | None

    def __init__(
        self,
        *,
        choices: Iterable | None = None,
        coerce=lambda val: val,
        strip: bool = True,
        key_field: Field | None = None,
        value_field: Field | None = None,
        **kwargs,
    ):
        self.choices = choices
        self.coerce = coerce
        self.strip = strip
        self.key_field = key_field
        self.value_field = value_field

        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result._choices = copy.deepcopy(self._choices, memo)
        return result

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value: Iterable | None):
        self._choices = set(value) if value else None

    choices: set[Any] | None = property(_get_choices, _set_choices)

    def to_python(self, data: dict | None) -> dict[str, str]:
        if not data:
            return {}
        elif not isinstance(data, dict):
            raise ValidationError(
                self.error_messages["invalid_dict"], code="invalid_dict"
            )

        cleaned_value = {}
        for key, value in data.items():
            key = key.strip()
            if not key:
                continue

            if self.strip:
                value = value.strip()

            cleaned_value[key] = value

        return cleaned_value

    def clean(self, value: dict[str, str]) -> dict:
        value = self.to_python(value)

        if self.coerce:
            value = self.coerce_keys(value)

        if self.key_field:
            value = self.clean_keys_with_field(value)

        if self.value_field:
            value = self.clean_values_with_field(value)

        self.validate(value)
        self.run_validators(value)
        return value

    def coerce_keys(self, data: dict) -> dict:
        cleaned_value = {}
        for key, value in data.items():
            try:
                key = self.coerce(key)
            except (ValueError, TypeError, ValidationError):
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": key},
                )
            cleaned_value[key] = value

        return cleaned_value

    def clean_keys_with_field(self, data: dict) -> dict:
        errors: list[ValidationError] = []
        cleaned_value = {}

        for key, value in data.items():
            try:
                key = self.key_field.clean(key)
                if key:
                    cleaned_value[key] = value
            except ValidationError as error:
                for message in error.messages:
                    errors.append(
                        ValidationError(
                            message=_(
                                "dict field key error", '"%(value)s": %(message)s'
                            ),
                            code="invalid_key",
                            params={"value": key, "message": message},
                        )
                    )

        if errors:
            raise ValidationError(errors)

        return cleaned_value

    def clean_values_with_field(self, data: dict) -> dict:
        errors: list[ValidationError] = []
        cleaned_value = {}

        for key, value in data.items():
            try:
                if c_value := self.value_field.clean(value):
                    cleaned_value[key] = c_value
            except ValidationError as error:
                for message in error.messages:
                    errors.append(
                        ValidationError(
                            message=_(
                                "dict field value error", '"%(value)s": %(message)s'
                            ),
                            code="invalid_value",
                            params={"value": value, "message": message},
                        )
                    )

        if errors:
            raise ValidationError(errors)

        return cleaned_value

    def validate(self, value: dict) -> dict:
        if self.required and not value:
            raise ValidationError(self.error_messages["required"], code="required")

        if self.choices:
            self.validate_against_choices(value)

    def validate_against_choices(self, value: dict) -> dict:
        for key in value:
            if key not in self.choices:
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": key},
                )

    def has_changed(self, initial: dict | None, data: dict | None) -> bool:
        if self.disabled:
            return False
        if initial is None:
            initial = {}
        if data is None:
            data = {}
        return initial != data


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
        value = self.to_python(value)

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

        self.validate(clean_data)
        self.run_validators(clean_data)
        return clean_data

    def validate(self, value: list):
        pass
