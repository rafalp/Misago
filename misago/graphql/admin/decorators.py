from functools import wraps
from inspect import isawaitable

from ...auth import get_authenticated_admin, get_authenticated_user
from .errors import AuthenticationGraphQLError, ForbiddenGraphQLError

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


def admin_resolver(f):
    @wraps(f)
    async def wrapper(obj, info, *args, **kwargs):
        auth = await get_authenticated_user(info.context)
        if not auth:
            raise AuthenticationGraphQLError()
        if not auth.is_administrator:
            raise ForbiddenGraphQLError()

        result = f(obj, info, *args, **kwargs)
        if isawaitable(result):
            result = await result
        return result

    return wrapper
