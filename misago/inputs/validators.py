from typing import Any, Callable, Optional, Sequence, Union

from .errors import Error, Errors, InputError


Validator = Callable[[Any, Optional[Errors], Optional[Any]], None]


class MinLengthValidator:
    _min_length: int

    def __init__(self, min_length: int):
        self._min_length = min_length

    def __call__(self, value: Sequence[Any], errors: Optional[Errors] = None):
        value_len = len(value)
        if value_len < self._min_length:
            raise InputError("TOO_SHORT", f"{value_len} < {self._min_length}")


def validate_min_length(min_length: int) -> MinLengthValidator:
    return MinLengthValidator(min_length)


class MaxLengthValidator:
    _max_length: int

    def __init__(self, max_length: int):
        self._max_length = max_length

    def __call__(self, value: Sequence[Any], errors: Optional[Errors] = None):
        value_len = len(value)
        if value_len > self._max_length:
            raise InputError("TOO_LONG", f"{value_len} > {self._max_length}")


def validate_max_length(max_length: int) -> MaxLengthValidator:
    return MaxLengthValidator(max_length)


class MinValueValidator:
    _min_value: int

    def __init__(self, min_value: int):
        self._min_value = min_value

    def __call__(self, value: Union[float, int], errors: Optional[Errors] = None):
        if value < self._min_value:
            raise InputError("TOO_SMALL", f"{value} < {self._min_value}")


def validate_min_value(min_value: int) -> MinValueValidator:
    return MinValueValidator(min_value)


class MaxValueValidator:
    _max_value: int

    def __init__(self, max_value: int):
        self._max_value = max_value

    def __call__(self, value: Union[float, int], errors: Optional[Errors] = None):
        if value > self._max_value:
            raise InputError("TOO_LARGE", f"{value} > {self._max_value}")


def validate_max_value(max_value: int) -> MaxValueValidator:
    return MaxValueValidator(max_value)


# TODO
# - URL
# - Email
# - Regex
# - One of
