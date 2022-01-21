from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadOpenInput = Dict[str, Any]
ThreadOpenInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], ThreadOpenInput, ErrorsList],
    Awaitable[Tuple[ThreadOpenInput, ErrorsList]],
]
ThreadOpenInputFilter = Callable[
    [ThreadOpenInputAction, GraphQLContext, ThreadOpenInput],
    Awaitable[Tuple[ThreadOpenInput, ErrorsList]],
]


class ThreadOpenInputHook(FilterHook[ThreadOpenInputAction, ThreadOpenInputFilter]):
    def call_action(
        self,
        action: ThreadOpenInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadOpenInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadOpenInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadOpenAction = Callable[[GraphQLContext, ThreadOpenInput], Awaitable[Thread]]
ThreadOpenFilter = Callable[
    [ThreadOpenAction, GraphQLContext, ThreadOpenInput],
    Awaitable[Thread],
]


class ThreadOpenHook(FilterHook[ThreadOpenAction, ThreadOpenFilter]):
    def call_action(
        self,
        action: ThreadOpenAction,
        context: GraphQLContext,
        cleaned_data: ThreadOpenInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_open_hook = ThreadOpenHook()
thread_open_input_hook = ThreadOpenInputHook()
