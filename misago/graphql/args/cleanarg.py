from typing import Any

from .exceptions import InvalidArgumentError


def clean_id_arg(value: Any) -> int:
    try:
        value = int(value)
        if value < 1:
            raise ValueError()
        return value
    except (TypeError, ValueError) as error:
        raise InvalidArgumentError() from error


def clean_page_arg(value: Any) -> int:
    if value is None:
        return 1

    try:
        value = int(value)
        if value < 1:
            raise ValueError()
        return value
    except (TypeError, ValueError) as error:
        raise InvalidArgumentError() from error
