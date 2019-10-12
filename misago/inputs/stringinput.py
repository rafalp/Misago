from typing import Any, List, Optional, Tuple

from .base import Input
from .errors import Error, ErrorsList, InputError
from .validators import Validator


class StringInput(Input):
    _allow_empty: bool
    _required: bool
    _strict: bool
    _strip: bool
    _validators: List[Validator]

    def __init__(
        self,
        *,
        allow_empty: bool = False,
        required: bool = True,
        strict: bool = False,
        strip: bool = True,
        validators: Optional[List[Validator]] = None,
    ):
        self._allow_empty = allow_empty
        self._required = required
        self._strict = strict
        self._strip = strip
        self._validators = validators or []

    def process(self, data: Any) -> Tuple[Optional[str], Optional[Error]]:
        try:
            cleaned_data = self.clean(data)
        except InputError as error:
            return None, ErrorsList([error])

        errors = ErrorsList()
        for validator in self._validators:
            try:
                validator(cleaned_data, errors)
            except InputError as error:
                errors.add_error(error)

        return cleaned_data, errors if errors else None

    def clean(self, data: Any) -> Optional[str]:
        if data is None:
            if self._required:
                raise InputError("REQUIRED")
            return None

        if not isinstance(data, str) and self._strict:
            raise InputError("INVALID")

        data = str(data)

        if self._strip:
            data = data.strip()

        if not data and not self._allow_empty:
            raise InputError("EMPTY")

        return data
