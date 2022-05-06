from typing import Any, Awaitable, Callable, Dict, List, Tuple

from ....context import Context
from ....hooks import FilterHook
from ....threads.models import Thread
from ....validation import ErrorsList, Validator

ThreadsBulkOpenInput = Dict[str, Any]
ThreadsBulkOpenInputAction = Callable[
    [
        Context,
        Dict[str, List[Validator]],
        ThreadsBulkOpenInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadsBulkOpenInput, ErrorsList]],
]
ThreadsBulkOpenInputFilter = Callable[
    [
        ThreadsBulkOpenInputAction,
        Context,
        ThreadsBulkOpenInput,
    ],
    Awaitable[Tuple[ThreadsBulkOpenInput, ErrorsList]],
]


class ThreadsBulkOpenInputHook(
    FilterHook[ThreadsBulkOpenInputAction, ThreadsBulkOpenInputFilter]
):
    def call_action(
        self,
        action: ThreadsBulkOpenInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkOpenInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadsBulkOpenInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadsBulkOpenAction = Callable[
    [Context, ThreadsBulkOpenInput], Awaitable[List[Thread]]
]
ThreadsBulkOpenFilter = Callable[
    [ThreadsBulkOpenAction, Context, ThreadsBulkOpenInput],
    Awaitable[List[Thread]],
]


class ThreadsBulkOpenHook(FilterHook[ThreadsBulkOpenAction, ThreadsBulkOpenFilter]):
    def call_action(
        self,
        action: ThreadsBulkOpenAction,
        context: Context,
        cleaned_data: ThreadsBulkOpenInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


threads_bulk_open_hook = ThreadsBulkOpenHook()
threads_bulk_open_input_hook = ThreadsBulkOpenInputHook()
