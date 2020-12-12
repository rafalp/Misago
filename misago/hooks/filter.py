from functools import reduce
from typing import Dict, Generic, List, TypeVar, cast


Action = TypeVar("Action")
Filter = TypeVar("Filter")


class FilterHook(Generic[Action, Filter]):
    is_async = True

    _cache: Dict[Action, Action]
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

    def async_wrap_action(self, action: Action) -> Action:
        def reduce_filter(action: Action, next_filter: Filter) -> Action:
            async def reduced_filter(*args, **kwargs):
                return await next_filter(action, *args, **kwargs)

            return cast(Action, reduced_filter)

        return reduce(reduce_filter, self._filters, action)

    def sync_wrap_action(self, action: Action) -> Action:
        def reduce_filter(action: Action, next_filter: Filter) -> Action:
            def reduced_filter(*args, **kwargs):
                return next_filter(action, *args, **kwargs)

            return cast(Action, reduced_filter)

        return reduce(reduce_filter, self._filters, action)

    def filter(self, action: Action, *args, **kwargs):
        if action not in self._cache:
            if self.is_async:
                self._cache[action] = self.async_wrap_action(action)
            else:
                self._cache[action] = self.sync_wrap_action(action)

        return self._cache[action](*args, **kwargs)  # type: ignore
