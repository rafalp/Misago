from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadRenameInput = Dict[str, Any]
ThreadRenameInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        ThreadRenameInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadRenameInput, ErrorsList]],
]
ThreadRenameInputFilter = Callable[
    [ThreadRenameInputAction, GraphQLContext, ThreadRenameInput],
    Awaitable[Tuple[ThreadRenameInput, ErrorsList]],
]


class ThreadRenameInputHook(
    FilterHook[ThreadRenameInputAction, ThreadRenameInputFilter]
):
    def call_action(
        self,
        action: ThreadRenameInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadRenameInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadRenameInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadRenameAction = Callable[[GraphQLContext, ThreadRenameInput], Awaitable[Thread]]
ThreadRenameFilter = Callable[
    [ThreadRenameAction, GraphQLContext, ThreadRenameInput], Awaitable[Thread]
]


class ThreadRenameHook(FilterHook[ThreadRenameAction, ThreadRenameFilter]):
    def call_action(
        self,
        action: ThreadRenameAction,
        context: GraphQLContext,
        cleaned_data: ThreadRenameInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_rename_hook = ThreadRenameHook()
thread_rename_input_hook = ThreadRenameInputHook()
