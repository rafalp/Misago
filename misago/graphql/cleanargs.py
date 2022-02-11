from functools import wraps
from inspect import isawaitable
from typing import Any, Optional, Tuple


class InvalidArgumentError(ValueError):
    pass


def clean_graphql_id(value: Any) -> int:
    try:
        value = int(value)
        if value < 1:
            raise ValueError()
        return value
    except (TypeError, ValueError) as error:
        raise InvalidArgumentError() from error


def clean_graphql_cursors(
    after: Any, before: Any
) -> Tuple[Optional[int], Optional[int]]:
    if after and before:
        raise InvalidArgumentError()

    if after:
        after = clean_graphql_cursor(after)
        return after, None

    if before:
        before = clean_graphql_cursor(before)
        return None, before

    return None, None


def clean_graphql_cursor(value: Any) -> Optional[int]:
    if value is None:
        return None

    try:
        value = int(value)
        if value < 0:
            raise ValueError()
        return value
    except (TypeError, ValueError) as error:
        raise InvalidArgumentError() from error


def clean_graphql_page(value: Any) -> int:
    if value is None:
        return 1

    try:
        value = int(value)
        if value < 1:
            raise ValueError()
        return value
    except (TypeError, ValueError) as error:
        raise InvalidArgumentError() from error


def invalid_args_result(f):
    """Returns None from decorated resolver when it raises InvalidArgumentError."""

    @wraps(f)
    async def wrap_resolver(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isawaitable(result):
                result = await result
        except InvalidArgumentError:
            return None

        return result

    return wrap_resolver
