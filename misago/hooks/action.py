from asyncio import gather
from typing import Generic, List, TypeVar


Action = TypeVar("Action")


class ActionHook(Generic[Action]):
    _actions: List[Action]

    def __init__(self):
        self._actions = []

    def append(self, action: Action):
        self._actions.append(action)

    def prepend(self, action: Action):
        self._actions.insert(0, action)

    async def gather(self, *args, **kwargs):
        if not self._actions:
            return []

        actions_calls = [action(*args, **kwargs) for action in self._actions]
        return await gather(*actions_calls)
