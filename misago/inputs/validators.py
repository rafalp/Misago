import re
from typing import Any, AnyStr, Callable, Optional, Pattern, Sequence, Union

from .errors import Error, Errors, InputError


Validator = Callable[[Any, Optional[Errors], Optional[Any]], None]


class MinLengthValidator:
    _min_length: int
    _code: str

    def __init__(self, min_length: int, *, code: str = "TOO_SHORT"):
        self._min_length = min_length
        self._code = code

    def __call__(self, value: Sequence[Any]):
        value_len = len(value)
        if value_len < self._min_length:
            raise InputError(self._code, f"{value_len} < {self._min_length}")


class MaxLengthValidator:
    _max_length: int
    _code: str

    def __init__(self, max_length: int, *, code: str = "TOO_LONG"):
        self._max_length = max_length
        self._code = code

    def __call__(self, value: Sequence[Any]):
        value_len = len(value)
        if value_len > self._max_length:
            raise InputError(self._code, f"{value_len} > {self._max_length}")


class MinValueValidator:
    _min_value: int
    _code: str

    def __init__(self, min_value: int, *, code: str = "TOO_SMALL"):
        self._min_value = min_value
        self._code = code

    def __call__(self, value: Union[float, int]):
        if value < self._min_value:
            raise InputError(self._code, f"{value} < {self._min_value}")


class MaxValueValidator:
    _max_value: int
    _code: str

    def __init__(self, max_value: int, *, code: str = "TOO_LARGE"):
        self._max_value = max_value
        self._code = code

    def __call__(self, value: Union[float, int]):
        if value > self._max_value:
            raise InputError(self._code, f"{value} > {self._max_value}")


class RegexValidator:
    _regex: Pattern[AnyStr]
    _code: str
    _flags: int
    _inverse_match: bool

    def __init__(
        self,
        regex: Union[str, Pattern[AnyStr]],
        *,
        code: str = "INVALID",
        flags: int = 0,
        inverse_match: bool = False,
    ):
        if flags and not isinstance(regex, str):
            raise TypeError(
                "'regex' argument must be string when 'flags' option is set"
            )

        self._regex = re.compile(regex, flags)
        self._code = code
        self._inverse_match = inverse_match

    def __call__(self, value: str):
        regex_matches = self._regex.search(value)
        invalid_input = regex_matches if self._inverse_match else not regex_matches
        if invalid_input:
            raise InputError(self._code)
