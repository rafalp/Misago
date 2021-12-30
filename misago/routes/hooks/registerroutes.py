from typing import Protocol

from starlette.applications import Starlette

from ...hooks import FilterHook


class RegisterRoutesAction(Protocol):
    def __call__(self, app: Starlette):
        ...


class RegisterRoutesFilter(Protocol):
    def __call__(self, action: RegisterRoutesAction, app: Starlette):
        ...


class RegisterRoutesHook(FilterHook[RegisterRoutesAction, RegisterRoutesFilter]):
    is_async = False

    def call_action(self, action: RegisterRoutesAction, app: Starlette):
        return self.filter(action, app)


register_routes_hook = RegisterRoutesHook()
