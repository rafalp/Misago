import functools
from asyncio import Future
from typing import Any, Awaitable, Callable, Dict, List, Sequence

from aiodataloader import DataLoader

from ..graphql import GraphQLContext
from ..utils.strings import parse_db_id

LoaderFunction = Callable[[Sequence[Any]], Awaitable[Sequence[Any]]]


def get_loader(
    context: GraphQLContext,
    name: str,
    loader_function: LoaderFunction,
    *,
    coerce_id_to=parse_db_id,
) -> DataLoader:
    context_key = get_loader_context_key(name)
    if context_key not in context:
        wrapped_loader_function = wrap_loader_function(loader_function, coerce_id_to)
        context[context_key] = DataLoader(wrapped_loader_function, get_cache_key=str)
    return context[context_key]


def get_loader_context_key(name: str) -> str:
    return f"__loader_{name}"


def wrap_loader_function(
    loader_function: LoaderFunction, coerce_id=parse_db_id
) -> LoaderFunction:
    async def wrapped_loader_function(ids: Sequence[Any]) -> List[Any]:
        data: Dict[str, Any] = {}
        graphql_ids = [str(i) for i in ids]
        internal_ids: List[Any] = []

        for graphql_id in graphql_ids:
            internal_id = coerce_id(graphql_id)
            if internal_id is not None:
                internal_ids.append(internal_id)
            else:
                data[graphql_id] = None
        if internal_ids:
            for item in await loader_function(internal_ids):
                data[str(item.id)] = item
        return [data.get(i) for i in graphql_ids]

    return wrapped_loader_function


def list_loader(cache_key: str):
    def wrap_list_loader(f):
        @functools.wraps(f)
        async def wrapped_list_loader_func(context: GraphQLContext):
            if cache_key not in context:
                future: Future[Any] = Future()
                context[cache_key] = future
                try:
                    future.set_result(await f(context))
                except Exception as e:  # pylint: disable=broad-except
                    future.set_exception(e)

            return await context[cache_key]

        return wrapped_list_loader_func

    return wrap_list_loader
