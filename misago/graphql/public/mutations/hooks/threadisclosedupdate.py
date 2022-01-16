from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadIsClosedUpdateInputModel = Type[BaseModel]
ThreadIsClosedUpdateInputModelAction = Callable[
    [GraphQLContext], Awaitable[ThreadIsClosedUpdateInputModel]
]
ThreadIsClosedUpdateInputModelFilter = Callable[
    [ThreadIsClosedUpdateInputModelAction, GraphQLContext],
    Awaitable[ThreadIsClosedUpdateInputModel],
]


class ThreadIsClosedUpdateInputModelHook(
    FilterHook[ThreadIsClosedUpdateInputModelAction, ThreadIsClosedUpdateInputModelFilter]
):
    def call_action(
        self, action: ThreadIsClosedUpdateInputModelAction, context: GraphQLContext
    ) -> Awaitable[ThreadIsClosedUpdateInputModel]:
        return self.filter(action, context)


ThreadIsClosedUpdateInput = Dict[str, Any]
ThreadIsClosedUpdateInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], ThreadIsClosedUpdateInput, ErrorsList],
    Awaitable[Tuple[ThreadIsClosedUpdateInput, ErrorsList]],
]
ThreadIsClosedUpdateInputFilter = Callable[
    [ThreadIsClosedUpdateInputAction, GraphQLContext, ThreadIsClosedUpdateInput],
    Awaitable[Tuple[ThreadIsClosedUpdateInput, ErrorsList]],
]


class ThreadIsClosedUpdateInputHook(FilterHook[ThreadIsClosedUpdateInputAction, ThreadIsClosedUpdateInputFilter]):
    def call_action(
        self,
        action: ThreadIsClosedUpdateInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadIsClosedUpdateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadIsClosedUpdateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadIsClosedUpdateAction = Callable[[GraphQLContext, ThreadIsClosedUpdateInput], Awaitable[Thread]]
ThreadIsClosedUpdateFilter = Callable[
    [ThreadIsClosedUpdateAction, GraphQLContext, ThreadIsClosedUpdateInput], Awaitable[Thread]
]


class ThreadIsClosedUpdateHook(FilterHook[ThreadIsClosedUpdateAction, ThreadIsClosedUpdateFilter]):
    def call_action(
        self,
        action: ThreadIsClosedUpdateAction,
        context: GraphQLContext,
        cleaned_data: ThreadIsClosedUpdateInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_is_closed_update_hook = ThreadIsClosedUpdateHook()
thread_is_closed_update_input_hook = ThreadIsClosedUpdateInputHook()
thread_is_closed_update_input_model_hook = ThreadIsClosedUpdateInputModelHook()
