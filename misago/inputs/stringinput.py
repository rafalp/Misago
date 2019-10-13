from typing import Any, Callable, List, Optional, Union

from .base import Input
from .errors import Error, ErrorsList, InputError
from .validators import Validator


class StringInput(Input):
    _allow_empty: bool
    _strip: bool

    _data_types = str

    def __init__(
        self,
        *,
        allow_empty: bool = False,
        default: Optional[Union[Callable[[], str], str]] = None,
        required: bool = True,
        strict: bool = False,
        strip: bool = True,
        validators: Optional[List[Validator]] = None,
    ):
        super().__init__(
            default=default, required=required, strict=strict, validators=validators
        )

        self._allow_empty = allow_empty
        self._strip = strip

    def clean(self, data: Any) -> Optional[str]:
        data = super().clean(data)

        if data is None:
            return None

        data = str(data)

        if self._strip:
            data = data.strip()

        if not data and not self._allow_empty:
            raise InputError("EMPTY")

        return data
