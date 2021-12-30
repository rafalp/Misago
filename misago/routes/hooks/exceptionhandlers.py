from typing import Protocol

from ...hooks import FilterHook


class ExceptionHandlersAction(Protocol):
    def __call__(self) -> dict:
        ...


class ExceptionHandlersFilter(Protocol):
    def __call__(self, action: ExceptionHandlersAction) -> dict:
        ...


class ExceptionHandlersHook(
    FilterHook[ExceptionHandlersAction, ExceptionHandlersFilter]
):
    is_async = False

    def call_action(self, action: ExceptionHandlersAction) -> dict:
        return self.filter(action)


exception_handlers_hook = ExceptionHandlersHook()
