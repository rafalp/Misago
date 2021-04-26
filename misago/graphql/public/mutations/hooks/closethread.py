from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....types import GraphQLContext, Thread, Validator

CloseThreadInputModel = Type[BaseModel]
CloseThreadInputModelAction = Callable[
    [GraphQLContext], Awaitable[CloseThreadInputModel]
]
CloseThreadInputModelFilter = Callable[
    [CloseThreadInputModelAction, GraphQLContext],
    Awaitable[CloseThreadInputModel],
]


class CloseThreadInputModelHook(
    FilterHook[CloseThreadInputModelAction, CloseThreadInputModelFilter]
):
    def call_action(
        self, action: CloseThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[CloseThreadInputModel]:
        return self.filter(action, context)


CloseThreadInput = Dict[str, Any]
CloseThreadInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], CloseThreadInput, ErrorsList],
    Awaitable[Tuple[CloseThreadInput, ErrorsList]],
]
CloseThreadInputFilter = Callable[
    [CloseThreadInputAction, GraphQLContext, CloseThreadInput],
    Awaitable[Tuple[CloseThreadInput, ErrorsList]],
]


class CloseThreadInputHook(FilterHook[CloseThreadInputAction, CloseThreadInputFilter]):
    def call_action(
        self,
        action: CloseThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: CloseThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[CloseThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


CloseThreadAction = Callable[[GraphQLContext, CloseThreadInput], Awaitable[Thread]]
CloseThreadFilter = Callable[
    [CloseThreadAction, GraphQLContext, CloseThreadInput], Awaitable[Thread]
]


class CloseThreadHook(FilterHook[CloseThreadAction, CloseThreadFilter]):
    def call_action(
        self,
        action: CloseThreadAction,
        context: GraphQLContext,
        cleaned_data: CloseThreadInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


close_thread_hook = CloseThreadHook()
close_thread_input_hook = CloseThreadInputHook()
close_thread_input_model_hook = CloseThreadInputModelHook()
