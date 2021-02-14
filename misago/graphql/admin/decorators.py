from functools import wraps
from inspect import isawaitable

from ...auth import get_authenticated_admin
from ...errors import NotAdminError


ERRORS = "errors"


def admin_query(f):
    @wraps(f)
    async def wrapper(obj, info, *args, **kwargs):
        if not await get_authenticated_admin(info.context):
            return None

        result = f(obj, info, *args, **kwargs)
        if isawaitable(result):
            result = await result
        return result

    return wrapper


def admin_mutation(f):
    @wraps(f)
    async def wrapper(obj, info, *args, **kwargs):
        if not await get_authenticated_admin(info.context):
            raise NotAdminError()

        result = f(obj, info, *args, **kwargs)
        if isawaitable(result):
            result = await result
        return result

    return wrapper
