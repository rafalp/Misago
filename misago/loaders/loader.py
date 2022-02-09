import functools
from asyncio import Future
from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    TypeVar,
)

from aiodataloader import DataLoader

from ..context import Context
from ..graphql import GraphQLContext
from ..utils.strings import parse_db_id
from .batchloadfunction import BatchLoadFunction

LoadedType = TypeVar("LoadedType")


@dataclass
class LoaderState:
    cache: dict
    loader: DataLoader


class Loader(Generic[LoadedType]):
    context_key: str

    def setup_context(self, context: Context) -> LoaderState:
        cache = {}
        state = LoaderState(
            cache=cache,
            loader=DataLoader(
                batch_load_fn=self.get_batch_load_function(),
                cache_map=cache,
            ),
        )

        context[self.context_key] = state
        return state

    def get_batch_load_function(self) -> BatchLoadFunction:
        raise NotImplementedError("Loader should override 'get_batch_load_function'")

    def get_loader(self, context: Context) -> DataLoader:
        return context[self.context_key].loader

    def load(self, context: Context, object_id: int) -> Awaitable[Optional[LoadedType]]:
        return self.get_loader(context).load(object_id)

    def load_many(
        self, context: Context, objects_ids: Iterable[int]
    ) -> Awaitable[List[Optional[LoadedType]]]:
        return self.get_loader(context).load_many(objects_ids)

    def store(self, context: Context, obj: LoadedType):
        loader = self.get_loader(context)
        loader.clear(obj.id)
        loader.prime(obj.id, obj)

    def store_many(self, context: Context, objects: Iterable[LoadedType]):
        loader = self.get_loader(context)
        for obj in objects:
            loader.clear(obj.id)
            loader.prime(obj.id, obj)

    def unload(self, context: Context, object_id: int):
        self.get_loader(context).clear(object_id)

    def unload_many(self, context: Context, objects_ids: Iterable[int]):
        loader = self.get_loader(context)
        for object_id in objects_ids:
            loader.clear(object_id)

    def unload_by_attr_value(self, context: Context, attr_name: str, attr_value: Any):
        cache = context[self.context_key].cache
        loader = context[self.context_key].loader

        for future in tuple(cache.values()):
            obj = future.result()
            if obj and getattr(obj, attr_name) == attr_value:
                loader.clear(obj.id)

    def unload_by_attr_value_in(
        self, context: Context, attr_name: str, attr_values: Iterable[Any]
    ):
        cache = context[self.context_key].cache
        loader = context[self.context_key].loader

        for future in tuple(cache.values()):
            obj = future.result()
            if obj and getattr(obj, attr_name) in attr_values:
                loader.clear(obj.id)

    def unload_all(self, context: Context):
        return self.get_loader(context).clear_all()


# DEPRECATED FUNCTIONS

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

            if not context[cache_key].done():
                await context[cache_key]

            return context[cache_key].result()

        return wrapped_list_loader_func

    return wrap_list_loader
