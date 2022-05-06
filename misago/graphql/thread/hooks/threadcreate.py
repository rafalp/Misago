from typing import Any, Awaitable, Callable, Dict, List, Tuple

from ....context import Context
from ....hooks import FilterHook
from ....richtext import ParsedMarkupMetadata
from ....threads.models import Post, Thread
from ....validation import ErrorsList, Validator

ThreadCreateInput = Dict[str, Any]
ThreadCreateInputAction = Callable[
    [
        Context,
        Dict[str, List[Validator]],
        ThreadCreateInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadCreateInput, ErrorsList]],
]
ThreadCreateInputFilter = Callable[
    [ThreadCreateInputAction, Context, ThreadCreateInput],
    Awaitable[Tuple[ThreadCreateInput, ErrorsList]],
]


class ThreadCreateInputHook(
    FilterHook[ThreadCreateInputAction, ThreadCreateInputFilter]
):
    def call_action(
        self,
        action: ThreadCreateInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadCreateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadCreateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadCreateAction = Callable[
    [Context, ThreadCreateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
ThreadCreateFilter = Callable[
    [ThreadCreateAction, Context, ThreadCreateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]


class ThreadCreateHook(FilterHook[ThreadCreateAction, ThreadCreateFilter]):
    def call_action(
        self,
        action: ThreadCreateAction,
        context: Context,
        cleaned_data: ThreadCreateInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


thread_create_hook = ThreadCreateHook()
thread_create_input_hook = ThreadCreateInputHook()
