from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadsIsClosedBulkUpdateInputModel = Type[BaseModel]
ThreadsIsClosedBulkUpdateInputModelAction = Callable[
    [GraphQLContext], Awaitable[ThreadsIsClosedBulkUpdateInputModel]
]
ThreadsIsClosedBulkUpdateInputModelFilter = Callable[
    [ThreadsIsClosedBulkUpdateInputModelAction, GraphQLContext],
    Awaitable[ThreadsIsClosedBulkUpdateInputModel],
]


class ThreadsIsClosedBulkUpdateInputModelHook(
    FilterHook[
        ThreadsIsClosedBulkUpdateInputModelAction,
        ThreadsIsClosedBulkUpdateInputModelFilter,
    ]
):
    def call_action(
        self, action: ThreadsIsClosedBulkUpdateInputModelAction, context: GraphQLContext
    ) -> Awaitable[ThreadsIsClosedBulkUpdateInputModel]:
        return self.filter(action, context)


ThreadsIsClosedBulkUpdateInput = Dict[str, Any]
ThreadsIsClosedBulkUpdateInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        ThreadsIsClosedBulkUpdateInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadsIsClosedBulkUpdateInput, ErrorsList]],
]
ThreadsIsClosedBulkUpdateInputFilter = Callable[
    [
        ThreadsIsClosedBulkUpdateInputAction,
        GraphQLContext,
        ThreadsIsClosedBulkUpdateInput,
    ],
    Awaitable[Tuple[ThreadsIsClosedBulkUpdateInput, ErrorsList]],
]


class ThreadsIsClosedBulkUpdateInputHook(
    FilterHook[
        ThreadsIsClosedBulkUpdateInputAction, ThreadsIsClosedBulkUpdateInputFilter
    ]
):
    def call_action(
        self,
        action: ThreadsIsClosedBulkUpdateInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadsIsClosedBulkUpdateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadsIsClosedBulkUpdateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadsIsClosedBulkUpdateAction = Callable[
    [GraphQLContext, ThreadsIsClosedBulkUpdateInput], Awaitable[List[Thread]]
]
ThreadsIsClosedBulkUpdateFilter = Callable[
    [ThreadsIsClosedBulkUpdateAction, GraphQLContext, ThreadsIsClosedBulkUpdateInput],
    Awaitable[List[Thread]],
]


class ThreadsIsClosedBulkUpdateHook(
    FilterHook[ThreadsIsClosedBulkUpdateAction, ThreadsIsClosedBulkUpdateFilter]
):
    def call_action(
        self,
        action: ThreadsIsClosedBulkUpdateAction,
        context: GraphQLContext,
        cleaned_data: ThreadsIsClosedBulkUpdateInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


threads_is_closed_bulk_update_hook = ThreadsIsClosedBulkUpdateHook()
threads_is_closed_bulk_update_input_hook = ThreadsIsClosedBulkUpdateInputHook()
threads_is_closed_bulk_update_input_model_hook = (
    ThreadsIsClosedBulkUpdateInputModelHook()
)
