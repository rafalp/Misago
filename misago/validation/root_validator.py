from functools import wraps
from inspect import isawaitable
from typing import Any, Dict

from .errors import VALIDATION_ERRORS
from .errorslist import ErrorsList


def root_validator(*, location: str):
    """Decorator for root validators that puts their errors at defined location"""

    def root_validator_wrapper(f):
        @wraps(f)
        async def wrapped_root_validator(
            data: Dict[str, Any], errors: ErrorsList, field_name: str
        ) -> Dict[str, Any]:
            try:
                result = f(data, errors, field_name)
                if isawaitable(result):
                    result = await result
                return result
            except VALIDATION_ERRORS as error:
                data.pop(location, None)
                errors.add_error(location, error)
                return data

        return wrapped_root_validator

    return root_validator_wrapper
