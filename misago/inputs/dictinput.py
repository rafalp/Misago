from typing import Any, Dict, Optional, Tuple

from .base import Input
from .errors import Error, ErrorsList, ErrorsMap, InputError


class DictInput(Input):
    _allow_empty: bool
    _fields: Dict[str, Input]
    _required: bool

    def __init__(
        self,
        fields: Optional[Dict[str, Input]] = None,
        *,
        allow_empty=False,
        required=True,
    ):
        self._allow_empty = allow_empty
        self._fields = fields or {}
        self._required = required

    def add_field(self, name: str, input_type: Input) -> Input:
        assert name not in self._fields, f"field '{name}' already exists"
        self._fields[name] = input_type
        return input_type

    def get_field(self, name: str, input_type: Input) -> Input:
        assert name in self._fields, f"field '{name}' doesn't exist"
        return self._fields[name]

    def get_fields(self) -> Dict[str, Input]:
        return self._fields

    def process(self, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Error]:
        try:
            data = self.clean(data)
        except InputError as error:
            return None, ErrorsList(error)

        if data is None:
            return None, None

        errors = ErrorsMap()
        cleaned_data = {}
        for field_name, field_input in self._fields.items():
            field_data, field_errors = field_input.process(data.get(field_name))

            if field_data:
                cleaned_data[field_name] = field_data
            if field_errors:
                errors.add_error(field_name, field_errors)

        return cleaned_data, errors

    def clean(self, data: Any) -> Optional[Dict[str, Any]]:
        if data is None:
            if self._required:
                raise InputError("REQUIRED")
            return None

        if not isinstance(data, dict) and self._strict:
            raise InputError("INVALID")

        if not data and not self._allow_empty:
            raise InputError("EMPTY")

        return data
