from asyncio import Future
from dataclasses import dataclass
from typing import Any, Awaitable, Dict, Generic, Iterable, List, Optional, TypeVar

from aiodataloader import DataLoader

from ..context import Context
from ..database import Model
from .batchloadfunction import BatchLoadFunction

LoadedType = TypeVar("LoadedType", bound=Model)


@dataclass
class LoaderState:
    cache: dict
    loader: DataLoader


class Loader(Generic[LoadedType]):
    context_key: str

    def setup_context(self, context: Context) -> LoaderState:
        cache: Dict[int, Future[LoadedType]] = {}
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
