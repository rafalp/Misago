from functools import wraps

from asgiref.sync import async_to_sync as async_to_sync_impl

from ..database import database


def uses_database(f):
    @wraps(f)
    def async_to_sync_wrapper(*args, **kwds):
        @async_to_sync_impl
        async def async_impl():
            async with database:
                return await f(*args, **kwds)

        return async_impl()

    return async_to_sync_wrapper
