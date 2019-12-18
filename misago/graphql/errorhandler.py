from functools import wraps
from typing import Union

from pydantic import PydanticTypeError, PydanticValueError

from ..types import AuthError, Error
from ..validation import get_error_dict


ERRORS = "errors"


def error_handler(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            result = await f(*args, **kwargs)
        except (AuthError, PydanticTypeError, PydanticValueError) as error:
            result = {ERRORS: [error]}

        if result.get(ERRORS):
            result[ERRORS] = [format_error(e) for e in result.get(ERRORS)]

        return result

    return wrapper


def format_error(error: Union[Error, Exception]) -> Error:
    if isinstance(error, Exception):
        return get_error_dict(error)
    return error
