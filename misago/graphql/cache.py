from asyncio import Future
from functools import wraps
from inspect import isawaitable
from typing import Any


def cached_resolver(f):
    cache_key = f"__cache_{f.__name__}"

    @wraps(f)
    async def resolver_with_cache(obj, info, *args, **kwargs):
        context = info.context
        if cache_key not in context:
            future: Future[Any] = Future()
            context[cache_key] = future
            try:
                result = f(obj, info, *args, **kwargs)
                if isawaitable(result):
                    result = await result
                future.set_result(result)
            except Exception as e:  # pylint: disable=broad-except
                future.set_exception(e)

        if not context[cache_key].done():
            await context[cache_key]

        return context[cache_key].result()

    return resolver_with_cache
