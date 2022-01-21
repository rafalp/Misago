from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadsBulkCloseInput = Dict[str, Any]
ThreadsBulkCloseInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        ThreadsBulkCloseInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadsBulkCloseInput, ErrorsList]],
]
ThreadsBulkCloseInputFilter = Callable[
    [
        ThreadsBulkCloseInputAction,
        GraphQLContext,
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
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkCloseInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadsBulkCloseInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadsBulkCloseAction = Callable[
    [GraphQLContext, ThreadsBulkCloseInput], Awaitable[List[Thread]]
]
ThreadsBulkCloseFilter = Callable[
    [ThreadsBulkCloseAction, GraphQLContext, ThreadsBulkCloseInput],
    Awaitable[List[Thread]],
]


class ThreadsBulkCloseHook(FilterHook[ThreadsBulkCloseAction, ThreadsBulkCloseFilter]):
    def call_action(
        self,
        action: ThreadsBulkCloseAction,
        context: GraphQLContext,
        cleaned_data: ThreadsBulkCloseInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


threads_bulk_close_hook = ThreadsBulkCloseHook()
threads_bulk_close_input_hook = ThreadsBulkCloseInputHook()
