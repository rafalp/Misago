import functools
import json
from asyncio import Future
from typing import Any

from ..context import Context


def simple_loader(cache_prefix: str):
    """Decorator that converts function into a loader."""

    def wrap_func(f):
        @functools.wraps(f)
        async def wrapped_func(context: Context, *args, **kwargs):
            cache_key = make_cache_key(cache_prefix, kwargs)
            if cache_key not in context:
                future: Future[Any] = Future()
                context[cache_key] = future
                try:
                    future.set_result(await f(context, *args, **kwargs))
                except Exception as e:  # pylint: disable=broad-except
                    future.set_exception(e)

            if not context[cache_key].done():
                await context[cache_key]

            return context[cache_key].result()

        return wrapped_func

    return wrap_func


def make_cache_key(cache_prefix: str, kwargs: dict) -> str:
    return f"_{cache_prefix}_cache:{json.dumps(kwargs)}"
