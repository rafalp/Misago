from functools import wraps
from inspect import isawaitable
from typing import Sequence, Union

from pydantic import PydanticTypeError, PydanticValueError

from ..errors import AuthError, ErrorDict, ErrorsList, get_error_dict


ERRORS = "errors"


def error_handler(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isawaitable(result):
                result = await result
        except (AuthError, PydanticTypeError, PydanticValueError) as error:
            result = {ERRORS: ErrorsList([format_error(error)])}

        if result.get(ERRORS):
            result[ERRORS] = ErrorsList([format_error(e) for e in result.get(ERRORS)])

        return result

    return wrapper


def format_error(error: Union[ErrorDict, Exception]) -> ErrorDict:
    if isinstance(error, Exception):
        error = get_error_dict(error)
    error["loc"] = format_error_location(error["loc"])
    return error


def format_error_location(
    error_location: Sequence[Union[str, int]]
) -> Sequence[Union[str, int]]:
    new_location = []
    for item in error_location:
        if isinstance(item, int) or item == ErrorsList.ROOT_LOCATION:
            new_location.append(item)
            continue

        new_location.append((item[0] + item.title()[1:]).replace("_", ""))

    return tuple(new_location)
