from functools import wraps
from inspect import isawaitable

from .errors import AuthenticationGraphQLError, ForbiddenGraphQLError


def admin_resolver(f):
    @wraps(f)
    async def wrapper(obj, info, *args, **kwargs):
        user = info.context["user"]
        if not user:
            raise AuthenticationGraphQLError()
        if not user.is_admin:
            raise ForbiddenGraphQLError()

        result = f(obj, info, *args, **kwargs)
        if isawaitable(result):
            result = await result
        return result

    return wrapper
