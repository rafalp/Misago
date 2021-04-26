from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....types import GraphQLContext, Thread, Validator

MoveThreadsInputModel = Type[BaseModel]
MoveThreadsInputModelAction = Callable[
    [GraphQLContext], Awaitable[MoveThreadsInputModel]
]
MoveThreadsInputModelFilter = Callable[
    [MoveThreadsInputModelAction, GraphQLContext],
    Awaitable[MoveThreadsInputModel],
]


class MoveThreadsInputModelHook(
    FilterHook[MoveThreadsInputModelAction, MoveThreadsInputModelFilter]
):
    def call_action(
        self, action: MoveThreadsInputModelAction, context: GraphQLContext
    ) -> Awaitable[MoveThreadsInputModel]:
        return self.filter(action, context)


MoveThreadsInput = Dict[str, Any]
MoveThreadsInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], MoveThreadsInput, ErrorsList],
    Awaitable[Tuple[MoveThreadsInput, ErrorsList]],
]
MoveThreadsInputFilter = Callable[
    [MoveThreadsInputAction, GraphQLContext, MoveThreadsInput],
    Awaitable[Tuple[MoveThreadsInput, ErrorsList]],
]


class MoveThreadsInputHook(FilterHook[MoveThreadsInputAction, MoveThreadsInputFilter]):
    def call_action(
        self,
        action: MoveThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: MoveThreadsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[MoveThreadsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


MoveThreadsAction = Callable[
    [GraphQLContext, MoveThreadsInput], Awaitable[List[Thread]]
]
MoveThreadsFilter = Callable[
    [MoveThreadsAction, GraphQLContext, MoveThreadsInput], Awaitable[List[Thread]]
]


class MoveThreadsHook(FilterHook[MoveThreadsAction, MoveThreadsFilter]):
    def call_action(
        self,
        action: MoveThreadsAction,
        context: GraphQLContext,
        cleaned_data: MoveThreadsInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


move_threads_hook = MoveThreadsHook()
move_threads_input_hook = MoveThreadsInputHook()
move_threads_input_model_hook = MoveThreadsInputModelHook()
