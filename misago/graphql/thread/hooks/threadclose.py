from typing import Any, Awaitable, Callable, Dict, List, Tuple

from ....context import Context
from ....hooks import FilterHook
from ....threads.models import Thread
from ....validation import ErrorsList, Validator

ThreadCloseInput = Dict[str, Any]
ThreadCloseInputAction = Callable[
    [Context, Dict[str, List[Validator]], ThreadCloseInput, ErrorsList],
    Awaitable[Tuple[ThreadCloseInput, ErrorsList]],
]
ThreadCloseInputFilter = Callable[
    [ThreadCloseInputAction, Context, ThreadCloseInput],
    Awaitable[Tuple[ThreadCloseInput, ErrorsList]],
]


class ThreadCloseInputHook(FilterHook[ThreadCloseInputAction, ThreadCloseInputFilter]):
    def call_action(
        self,
        action: ThreadCloseInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadCloseInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadCloseInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadCloseAction = Callable[[Context, ThreadCloseInput], Awaitable[Thread]]
ThreadCloseFilter = Callable[
    [ThreadCloseAction, Context, ThreadCloseInput],
    Awaitable[Thread],
]


class ThreadCloseHook(FilterHook[ThreadCloseAction, ThreadCloseFilter]):
    def call_action(
        self,
        action: ThreadCloseAction,
        context: Context,
        cleaned_data: ThreadCloseInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_close_hook = ThreadCloseHook()
thread_close_input_hook = ThreadCloseInputHook()
