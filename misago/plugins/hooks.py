from functools import reduce
from typing import Any, Generic, List, TypeVar, cast

Action = TypeVar("Action")
Filter = TypeVar("Filter")


class ActionHook(Generic[Action]):
    __slots__ = ("actions_first", "actions_last", "cache")

    actions_first: List[Action]
    actions_last: List[Action]
    cache: List[Action] | None

    def __init__(self):
        self.actions_first = []
        self.actions_last = []
        self.cache = None

    def append(self, action: Action):
        self.actions_last.append(action)
        self.invalidate_cache()

    def prepend(self, action: Action):
        self.actions_first.insert(0, action)
        self.invalidate_cache()

    def invalidate_cache(self):
        self.cache = None

    def __call__(self, *args, **kwargs) -> List[Any]:
        if self.cache is None:
            self.cache = self.actions_first + self.actions_last
        if not self.cache:
            return []

        return [action(*args, **kwargs) for action in self.cache]


class FilterHook(Generic[Action, Filter]):
    __slots__ = ("filters_first", "filters_last", "cache")

    filters_first: List[Filter]
    filters_last: List[Filter]
    cache: Action | None

    def __init__(self):
        self.filters_first = []
        self.filters_last = []
        self.cache = None

    def append(self, filter_: Filter):
        self.filters_last.append(filter_)
        self.invalidate_cache()

    def prepend(self, filter_: Filter):
        self.filters_first.insert(0, filter_)
        self.invalidate_cache()

    def invalidate_cache(self):
        self.cache = None

    def get_reduced_action(self, action: Action) -> Action:
        def reduce_filter(action: Action, next_filter: Filter) -> Action:
            def reduced_filter(*args, **kwargs):
                return next_filter(action, *args, **kwargs)

            return cast(Action, reduced_filter)

        filters = self.filters_first + self.filters_last
        return reduce(reduce_filter, filters, action)

    def __call__(self, action: Action, *args, **kwargs):
        if self.cache is None:
            self.cache = self.get_reduced_action(action)

        return self.cache(*args, **kwargs)  # type: ignore
