from functools import reduce
from typing import Any, Generic, List, TypeVar, cast

Action = TypeVar("Action")
Filter = TypeVar("Filter")


class ActionHook(Generic[Action]):
    actions: List[Action]

    def __init__(self):
        self.actions = []

    def append(self, action: Action):
        self.actions.append(action)

    def prepend(self, action: Action):
        self.actions.insert(0, action)

    def call(self, *args, **kwargs) -> List[Any]:
        if not self.actions:
            return []

        return [action(*args, **kwargs) for action in self.actions]


class FilterHook(Generic[Action, Filter]):
    cache: Action | None
    filters: List[Filter]

    def __init__(self):
        self.cache = None
        self.filters = []

    def append(self, filter_: Filter):
        self.filters.append(filter_)
        self.invalidate_cache()

    def prepend(self, filter_: Filter):
        self.filters.insert(0, filter_)
        self.invalidate_cache()

    def invalidate_cache(self):
        self.cache = None

    def get_reduced_action(self, action: Action) -> Action:
        def reduce_filter(action: Action, next_filter: Filter) -> Action:
            def reduced_filter(*args, **kwargs):
                return next_filter(action, *args, **kwargs)

            return cast(Action, reduced_filter)

        return reduce(reduce_filter, self.filters, action)

    def filter(self, action: Action, *args, **kwargs):
        if self.cache is None:
            self.cache = self.get_reduced_action(action)

        return self.cache(*args, **kwargs)  # type: ignore
