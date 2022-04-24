from typing import Any, Optional, Tuple

from .exceptions import InvalidArgumentError


def clean_id_arg(value: Any) -> int:
    try:
        value = int(value)
        if value < 1:
            raise ValueError()
        return value
    except (TypeError, ValueError) as error:
        raise InvalidArgumentError() from error


def clean_cursors_args(after: Any, before: Any) -> Tuple[Optional[int], Optional[int]]:
    if after and before:
        raise InvalidArgumentError()

    if after:
        after = clean_cursor_arg(after)
        return after, None

    if before:
        before = clean_cursor_arg(before)
        return None, before

    return None, None


def clean_cursor_arg(value: Any) -> Optional[int]:
    if value is None:
        return None

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
