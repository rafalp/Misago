from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadTitleUpdateInputModel = Type[BaseModel]
ThreadTitleUpdateInputModelAction = Callable[
    [GraphQLContext], Awaitable[ThreadTitleUpdateInputModel]
]
ThreadTitleUpdateInputModelFilter = Callable[
    [ThreadTitleUpdateInputModelAction, GraphQLContext],
    Awaitable[ThreadTitleUpdateInputModel],
]


class ThreadTitleUpdateInputModelHook(
    FilterHook[ThreadTitleUpdateInputModelAction, ThreadTitleUpdateInputModelFilter]
):
    def call_action(
        self, action: ThreadTitleUpdateInputModelAction, context: GraphQLContext
    ) -> Awaitable[ThreadTitleUpdateInputModel]:
        return self.filter(action, context)


ThreadTitleUpdateInput = Dict[str, Any]
ThreadTitleUpdateInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        ThreadTitleUpdateInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadTitleUpdateInput, ErrorsList]],
]
ThreadTitleUpdateInputFilter = Callable[
    [ThreadTitleUpdateInputAction, GraphQLContext, ThreadTitleUpdateInput],
    Awaitable[Tuple[ThreadTitleUpdateInput, ErrorsList]],
]


class ThreadTitleUpdateInputHook(
    FilterHook[ThreadTitleUpdateInputAction, ThreadTitleUpdateInputFilter]
):
    def call_action(
        self,
        action: ThreadTitleUpdateInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadTitleUpdateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadTitleUpdateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadTitleUpdateAction = Callable[
    [GraphQLContext, ThreadTitleUpdateInput], Awaitable[Thread]
]
ThreadTitleUpdateFilter = Callable[
    [ThreadTitleUpdateAction, GraphQLContext, ThreadTitleUpdateInput], Awaitable[Thread]
]


class ThreadTitleUpdateHook(
    FilterHook[ThreadTitleUpdateAction, ThreadTitleUpdateFilter]
):
    def call_action(
        self,
        action: ThreadTitleUpdateAction,
        context: GraphQLContext,
        cleaned_data: ThreadTitleUpdateInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_title_update_hook = ThreadTitleUpdateHook()
thread_title_update_input_hook = ThreadTitleUpdateInputHook()
thread_title_update_input_model_hook = ThreadTitleUpdateInputModelHook()
