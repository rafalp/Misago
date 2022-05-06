from typing import Any, Awaitable, Callable, Dict, List, Tuple

from ....context import Context
from ....hooks import FilterHook
from ....threads.models import Thread
from ....validation import ErrorsList, Validator

ThreadsBulkMoveInput = Dict[str, Any]
ThreadsBulkMoveInputAction = Callable[
    [Context, Dict[str, List[Validator]], ThreadsBulkMoveInput, ErrorsList],
    Awaitable[Tuple[ThreadsBulkMoveInput, ErrorsList]],
]
ThreadsBulkMoveInputFilter = Callable[
    [ThreadsBulkMoveInputAction, Context, ThreadsBulkMoveInput],
    Awaitable[Tuple[ThreadsBulkMoveInput, ErrorsList]],
]


class ThreadsBulkMoveInputHook(
    FilterHook[ThreadsBulkMoveInputAction, ThreadsBulkMoveInputFilter]
):
    def call_action(
        self,
        action: ThreadsBulkMoveInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkMoveInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadsBulkMoveInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadsBulkMoveAction = Callable[
    [Context, ThreadsBulkMoveInput], Awaitable[List[Thread]]
]
ThreadsBulkMoveFilter = Callable[
    [ThreadsBulkMoveAction, Context, ThreadsBulkMoveInput],
    Awaitable[List[Thread]],
]


class ThreadsBulkMoveHook(FilterHook[ThreadsBulkMoveAction, ThreadsBulkMoveFilter]):
    def call_action(
        self,
        action: ThreadsBulkMoveAction,
        context: Context,
        cleaned_data: ThreadsBulkMoveInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


threads_bulk_move_hook = ThreadsBulkMoveHook()
threads_bulk_move_input_hook = ThreadsBulkMoveInputHook()
