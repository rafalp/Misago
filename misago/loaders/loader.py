from typing import Any, Awaitable, Callable, List, Sequence

from aiodataloader import DataLoader

from ..types import GraphQLContext


LoaderFunction = Callable[[Sequence[Any]], Awaitable[Sequence[Any]]]


def get_loader(
    context: GraphQLContext, name: str, loader_function: LoaderFunction,
) -> DataLoader:
    context_key = f"__loader_{name}"
    if context_key not in context:
        wrapped_loader_function = wrap_loader_function(loader_function)
        context[context_key] = DataLoader(wrapped_loader_function)
    return context[context_key]


def wrap_loader_function(loader_function: LoaderFunction) -> LoaderFunction:
    async def wrapped_loader_function(ids: Sequence[Any]) -> List[Any]:
        data_map = {r.id: r for r in await loader_function(ids)}
        return [data_map.get(i) for i in ids]

    return wrapped_loader_function
