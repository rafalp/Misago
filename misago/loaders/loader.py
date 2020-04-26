from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence

from aiodataloader import DataLoader

from ..types import GraphQLContext
from ..utils.strings import parse_db_id


LoaderFunction = Callable[[Sequence[Any]], Awaitable[Sequence[Any]]]


def get_loader(
    context: GraphQLContext,
    name: str,
    loader_function: LoaderFunction,
    *,
    coerce_id_to=parse_db_id,
) -> DataLoader:
    context_key = f"__loader_{name}"
    if context_key not in context:
        wrapped_loader_function = wrap_loader_function(loader_function, coerce_id_to)
        context[context_key] = DataLoader(wrapped_loader_function, get_cache_key=str)
    return context[context_key]


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
