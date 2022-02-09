from functools import wraps
from typing import Any, Awaitable, Callable, Dict, List, Sequence, Union


BatchLoadFunction = Callable[[Sequence[Any]], Awaitable[Sequence[Any]]]
Id = Union[str, int]


def batch_load_function(fn: BatchLoadFunction) -> BatchLoadFunction:
    @wraps(fn)
    async def wrapped_function(ids: Sequence[Any]) -> List[Any]:
        data: Dict[str, Any] = {}
        graphql_ids = [str(i) for i in ids]
        internal_ids: List[Any] = []

        for graphql_id in graphql_ids:
            internal_id = int(graphql_id)
            if internal_id is not None:
                internal_ids.append(internal_id)
            else:
                data[graphql_id] = None
        if internal_ids:
            for item in await fn(internal_ids):
                data[str(item.id)] = item
        return [data.get(i) for i in graphql_ids]

    return wrapped_function
