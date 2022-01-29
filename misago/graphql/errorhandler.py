from functools import wraps
from inspect import isawaitable
from typing import Union

from ..validation import VALIDATION_ERRORS, ErrorDict, ErrorsList, get_error_dict

ERRORS = "errors"


def error_handler(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isawaitable(result):
                result = await result
        except VALIDATION_ERRORS as error:
            result = {ERRORS: ErrorsList([format_error(error)])}

        if result.get(ERRORS):
            result[ERRORS] = ErrorsList([format_error(e) for e in result.get(ERRORS)])

        return result

    return wrapper


def format_error(error: Union[ErrorDict, Exception]) -> ErrorDict:
    if isinstance(error, Exception):
        return get_error_dict(error)
    return error
