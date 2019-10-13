from typing import Any, List, Optional, Tuple

from .errors import Error, ErrorsList, InputError
from .validators import Validator


class Input:
    _default: Any
    _required: bool
    _strict: bool
    _validators: List[Validator]

    _data_types: Any

    def __init__(
        self,
        *,
        default: Optional[Any] = None,
        required: bool = True,
        strict: bool = True,
        validators: Optional[List[Validator]] = None,
    ):
        self._default = default
        self._required = required
        self._strict = strict
        self._validators = validators or []

    def process(self, data: Any) -> Tuple[Optional[str], Optional[Error]]:
        try:
            cleaned_data = self.clean(data)
        except InputError as error:
            return None, ErrorsList([error])

        if cleaned_data is not None:
            return cleaned_data, self.validate(cleaned_data)

        return self.get_default_value(), ErrorsList()

    def clean(self, data: Any) -> Any:
        if data is None:
            if self._required:
                raise InputError("REQUIRED")
            return None

        if self._strict and not self._data_types:
            raise TypeError(
                "'strict' option is enabled, but '_data_types' attribute is not set."
                f"Add '_data_types' attribute to '{self.__class__.__name__}'."
            )

        if not isinstance(data, self._data_types) and self._strict:
            raise InputError("INVALID")

        return data

    def get_default_value(self) -> Any:
        if callable(self._default):
            return self._default()
        return self._default

    def validate(self, data: Any) -> ErrorsList:
        errors = ErrorsList()

        for validator in self._validators:
            try:
                validator(data)
            except InputError as error:
                errors.add_error(error)

        return errors
