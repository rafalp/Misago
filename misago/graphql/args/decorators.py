from functools import wraps
from inspect import isawaitable

from .exceptions import InvalidArgumentError


def handle_invalid_args(f):
    """Returns None from decorated resolver when it raises InvalidArgumentError."""

    @wraps(f)
    async def wrap_resolver(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isawaitable(result):
                return await result
            return result
        except InvalidArgumentError:
            return None

    return wrap_resolver
