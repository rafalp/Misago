from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadMoveInput = Dict[str, Any]
ThreadMoveInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], ThreadMoveInput, ErrorsList],
    Awaitable[Tuple[ThreadMoveInput, ErrorsList]],
]
ThreadMoveInputFilter = Callable[
    [ThreadMoveInputAction, GraphQLContext, ThreadMoveInput],
    Awaitable[Tuple[ThreadMoveInput, ErrorsList]],
]


class ThreadMoveInputHook(FilterHook[ThreadMoveInputAction, ThreadMoveInputFilter]):
    def call_action(
        self,
        action: ThreadMoveInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadMoveInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadMoveInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadMoveAction = Callable[[GraphQLContext, ThreadMoveInput], Awaitable[Thread]]
ThreadMoveFilter = Callable[
    [ThreadMoveAction, GraphQLContext, ThreadMoveInput],
    Awaitable[Thread],
]


class ThreadMoveHook(FilterHook[ThreadMoveAction, ThreadMoveFilter]):
    def call_action(
        self,
        action: ThreadMoveAction,
        context: GraphQLContext,
        cleaned_data: ThreadMoveInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_move_hook = ThreadMoveHook()
thread_move_input_hook = ThreadMoveInputHook()
