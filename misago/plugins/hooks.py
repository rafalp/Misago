from functools import reduce
from typing import Any, Generic, List, TypeVar, cast

Action = TypeVar("Action")
Filter = TypeVar("Filter")


class ActionHook(Generic[Action]):
    __slots__ = ("_actions_first", "_actions_last", "_cache")

    _actions_first: List[Action]
    _actions_last: List[Action]
    _cache: List[Action] | None

    def __init__(self):
        self.clear_actions()

    def __bool__(self) -> bool:
        return bool(self._actions_first or self._actions_last)

    def clear_actions(self):
        self._actions_first = []
        self._actions_last = []
        self._cache = None

    def append_action(self, action: Action):
        self._actions_last.append(action)
        self.invalidate_cache()

    def prepend_action(self, action: Action):
        self._actions_first.insert(0, action)
        self.invalidate_cache()

    def invalidate_cache(self):
        self._cache = None

    def __call__(self, *args, **kwargs) -> List[Any]:
        if self._cache is None:
            self._cache = self._actions_first + self._actions_last
        if not self._cache:
            return []

        return [action(*args, **kwargs) for action in self._cache]


class FilterHook(Generic[Action, Filter]):
    __slots__ = ("cache", "_filters_first", "_filters_last", "_use_filters", "_cache")

    cache: bool

    _filters_first: List[Filter]
    _filters_last: List[Filter]
    _use_filters: bool
    _cache: Action | None

    def __init__(self, cache: bool = True):
        self.cache = cache
        self.clear_actions()

    def __bool__(self) -> bool:
        return bool(self._filters_first or self._filters_last)

    def clear_actions(self):
        self._filters_first = []
        self._filters_last = []
        self._use_filters = False
        self._cache = None

    def append_filter(self, filter_: Filter):
        self._filters_last.append(filter_)
        self._use_filters = True
        self.invalidate_cache()

    def prepend_filter(self, filter_: Filter):
        self._filters_first.insert(0, filter_)
        self._use_filters = True
        self.invalidate_cache()

    def invalidate_cache(self):
        self._cache = None

    def get_reduced_action(self, action: Action) -> Action:
        def reduce_filter(action: Action, next_filter: Filter) -> Action:
            def reduced_filter(*args, **kwargs):
                return next_filter(action, *args, **kwargs)

            return cast(Action, reduced_filter)

        filters = self._filters_first + self._filters_last
        return reduce(reduce_filter, filters, action)

    def __call__(self, action: Action, *args, **kwargs):
        if not self._use_filters:
            return action(*args, **kwargs)

        if not self.cache:
            reduced_action = self.get_reduced_action(action)
            return reduced_action(*args, **kwargs)

        if self._cache is None:
            self._cache = self.get_reduced_action(action)

        return self._cache(*args, **kwargs)  # type: ignore
