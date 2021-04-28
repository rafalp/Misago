from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

CloseThreadsInputModel = Type[BaseModel]
CloseThreadsInputModelAction = Callable[
    [GraphQLContext], Awaitable[CloseThreadsInputModel]
]
CloseThreadsInputModelFilter = Callable[
    [CloseThreadsInputModelAction, GraphQLContext],
    Awaitable[CloseThreadsInputModel],
]


class CloseThreadsInputModelHook(
    FilterHook[CloseThreadsInputModelAction, CloseThreadsInputModelFilter]
):
    def call_action(
        self, action: CloseThreadsInputModelAction, context: GraphQLContext
    ) -> Awaitable[CloseThreadsInputModel]:
        return self.filter(action, context)


CloseThreadsInput = Dict[str, Any]
CloseThreadsInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], CloseThreadsInput, ErrorsList],
    Awaitable[Tuple[CloseThreadsInput, ErrorsList]],
]
CloseThreadsInputFilter = Callable[
    [CloseThreadsInputAction, GraphQLContext, CloseThreadsInput],
    Awaitable[Tuple[CloseThreadsInput, ErrorsList]],
]


class CloseThreadsInputHook(
    FilterHook[CloseThreadsInputAction, CloseThreadsInputFilter]
):
    def call_action(
        self,
        action: CloseThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: CloseThreadsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[CloseThreadsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


CloseThreadsAction = Callable[
    [GraphQLContext, CloseThreadsInput], Awaitable[List[Thread]]
]
CloseThreadsFilter = Callable[
    [CloseThreadsAction, GraphQLContext, CloseThreadsInput], Awaitable[List[Thread]]
]


class CloseThreadsHook(FilterHook[CloseThreadsAction, CloseThreadsFilter]):
    def call_action(
        self,
        action: CloseThreadsAction,
        context: GraphQLContext,
        cleaned_data: CloseThreadsInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


close_threads_hook = CloseThreadsHook()
close_threads_input_hook = CloseThreadsInputHook()
close_threads_input_model_hook = CloseThreadsInputModelHook()
