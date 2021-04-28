from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....types import Validator
from .... import GraphQLContext

MoveThreadInputModel = Type[BaseModel]
MoveThreadInputModelAction = Callable[[GraphQLContext], Awaitable[MoveThreadInputModel]]
MoveThreadInputModelFilter = Callable[
    [MoveThreadInputModelAction, GraphQLContext],
    Awaitable[MoveThreadInputModel],
]


class MoveThreadInputModelHook(
    FilterHook[MoveThreadInputModelAction, MoveThreadInputModelFilter]
):
    def call_action(
        self, action: MoveThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[MoveThreadInputModel]:
        return self.filter(action, context)


MoveThreadInput = Dict[str, Any]
MoveThreadInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], MoveThreadInput, ErrorsList],
    Awaitable[Tuple[MoveThreadInput, ErrorsList]],
]
MoveThreadInputFilter = Callable[
    [MoveThreadInputAction, GraphQLContext, MoveThreadInput],
    Awaitable[Tuple[MoveThreadInput, ErrorsList]],
]


class MoveThreadInputHook(FilterHook[MoveThreadInputAction, MoveThreadInputFilter]):
    def call_action(
        self,
        action: MoveThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: MoveThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[MoveThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


MoveThreadAction = Callable[[GraphQLContext, MoveThreadInput], Awaitable[Thread]]
MoveThreadFilter = Callable[
    [MoveThreadAction, GraphQLContext, MoveThreadInput], Awaitable[Thread]
]


class MoveThreadHook(FilterHook[MoveThreadAction, MoveThreadFilter]):
    def call_action(
        self,
        action: MoveThreadAction,
        context: GraphQLContext,
        cleaned_data: MoveThreadInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


move_thread_hook = MoveThreadHook()
move_thread_input_hook = MoveThreadInputHook()
move_thread_input_model_hook = MoveThreadInputModelHook()
