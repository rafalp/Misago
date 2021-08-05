from functools import wraps
from inspect import isawaitable

from ...auth import get_authenticated_user
from .errors import AuthenticationGraphQLError, ForbiddenGraphQLError


def admin_resolver(f):
    @wraps(f)
    async def wrapper(obj, info, *args, **kwargs):
        auth = await get_authenticated_user(info.context)
        if not auth:
            raise AuthenticationGraphQLError()
        if not auth.is_admin:
            raise ForbiddenGraphQLError()

        result = f(obj, info, *args, **kwargs)
        if isawaitable(result):
            result = await result
        return result

    return wrapper
