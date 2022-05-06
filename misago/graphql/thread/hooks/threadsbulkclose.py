from typing import Any, Awaitable, Callable, Dict, List, Tuple

from ....context import Context
from ....hooks import FilterHook
from ....threads.models import Thread
from ....validation import ErrorsList, Validator

ThreadsBulkCloseInput = Dict[str, Any]
ThreadsBulkCloseInputAction = Callable[
    [
        Context,
        Dict[str, List[Validator]],
        ThreadsBulkCloseInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadsBulkCloseInput, ErrorsList]],
]
ThreadsBulkCloseInputFilter = Callable[
    [
        ThreadsBulkCloseInputAction,
        Context,
        ThreadsBulkCloseInput,
    ],
    Awaitable[Tuple[ThreadsBulkCloseInput, ErrorsList]],
]


class ThreadsBulkCloseInputHook(
    FilterHook[ThreadsBulkCloseInputAction, ThreadsBulkCloseInputFilter]
):
    def call_action(
        self,
        action: ThreadsBulkCloseInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkCloseInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadsBulkCloseInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadsBulkCloseAction = Callable[
    [Context, ThreadsBulkCloseInput], Awaitable[List[Thread]]
]
ThreadsBulkCloseFilter = Callable[
    [ThreadsBulkCloseAction, Context, ThreadsBulkCloseInput],
    Awaitable[List[Thread]],
]


class ThreadsBulkCloseHook(FilterHook[ThreadsBulkCloseAction, ThreadsBulkCloseFilter]):
    def call_action(
        self,
        action: ThreadsBulkCloseAction,
        context: Context,
        cleaned_data: ThreadsBulkCloseInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


threads_bulk_close_hook = ThreadsBulkCloseHook()
threads_bulk_close_input_hook = ThreadsBulkCloseInputHook()
