from functools import wraps
from typing import Union

from pydantic import PydanticTypeError, PydanticValueError

from ..errors import AuthError, ErrorDict, ErrorsList, get_error_dict


ERRORS = "errors"


def error_handler(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            result = await f(*args, **kwargs)
        except (AuthError, PydanticTypeError, PydanticValueError) as error:
            result = {ERRORS: ErrorsList([format_error(error)])}

        if result.get(ERRORS):
            result[ERRORS] = ErrorsList([format_error(e) for e in result.get(ERRORS)])

        return result

    return wrapper


def format_error(error: Union[ErrorDict, Exception]) -> ErrorDict:
    if isinstance(error, Exception):
        return get_error_dict(error)
    return error
