from functools import reduce
from typing import Dict, Generic, List, TypeVar, cast


Action = TypeVar("Action")
Filter = TypeVar("Filter")


class FilterHook(Generic[Action, Filter]):
    _cache: Dict[int, Action]
    _filters: List[Filter]

    def __init__(self):
        self._cache = {}
        self._filters = []

    def append(self, filter_: Filter):
        self._filters.append(filter_)
        self.invalidate_cache()

    def prepend(self, filter_: Filter):
        self._filters.insert(0, filter_)
        self.invalidate_cache()

    def invalidate_cache(self):
        self._cache = {}

    def wrap_action(self, action: Action) -> Action:
        def reduce_filter(action: Action, next_filter: Filter) -> Action:
            async def reduced_filter(*args, **kwargs):
                return await next_filter(action, *args, **kwargs)

            return cast(Action, reduced_filter)

        return reduce(reduce_filter, self._filters, action)

    async def filter(self, action: Action, *args, **kwargs):
        action_id = id(action)
        if action_id not in self._cache:
            self._cache[action_id] = self.wrap_action(action)
        return await self._cache[action_id](*args, **kwargs)  # type: ignore
