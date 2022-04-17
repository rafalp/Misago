from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....context import Context
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import ErrorsList, Validator

ThreadOpenInput = Dict[str, Any]
ThreadOpenInputAction = Callable[
    [Context, Dict[str, List[Validator]], ThreadOpenInput, ErrorsList],
    Awaitable[Tuple[ThreadOpenInput, ErrorsList]],
]
ThreadOpenInputFilter = Callable[
    [ThreadOpenInputAction, Context, ThreadOpenInput],
    Awaitable[Tuple[ThreadOpenInput, ErrorsList]],
]


class ThreadOpenInputHook(FilterHook[ThreadOpenInputAction, ThreadOpenInputFilter]):
    def call_action(
        self,
        action: ThreadOpenInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadOpenInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadOpenInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadOpenAction = Callable[[Context, ThreadOpenInput], Awaitable[Thread]]
ThreadOpenFilter = Callable[
    [ThreadOpenAction, Context, ThreadOpenInput],
    Awaitable[Thread],
]


class ThreadOpenHook(FilterHook[ThreadOpenAction, ThreadOpenFilter]):
    def call_action(
        self,
        action: ThreadOpenAction,
        context: Context,
        cleaned_data: ThreadOpenInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_open_hook = ThreadOpenHook()
thread_open_input_hook = ThreadOpenInputHook()
