from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....types import Validator
from .... import GraphQLContext

DeleteThreadsInputModel = Type[BaseModel]
DeleteThreadsInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadsInputModel]
]
DeleteThreadsInputModelFilter = Callable[
    [DeleteThreadsInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadsInputModel],
]


class DeleteThreadsInputModelHook(
    FilterHook[DeleteThreadsInputModelAction, DeleteThreadsInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadsInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadsInputModel]:
        return self.filter(action, context)


DeleteThreadsInput = Dict[str, Any]
DeleteThreadsInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], DeleteThreadsInput, ErrorsList],
    Awaitable[Tuple[DeleteThreadsInput, ErrorsList]],
]
DeleteThreadsInputFilter = Callable[
    [DeleteThreadsInputAction, GraphQLContext, DeleteThreadsInput],
    Awaitable[Tuple[DeleteThreadsInput, ErrorsList]],
]


class DeleteThreadsInputHook(
    FilterHook[DeleteThreadsInputAction, DeleteThreadsInputFilter]
):
    def call_action(
        self,
        action: DeleteThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


DeleteThreadsAction = Callable[[GraphQLContext, DeleteThreadsInput], Awaitable[None]]
DeleteThreadsFilter = Callable[
    [DeleteThreadsAction, GraphQLContext, DeleteThreadsInput], Awaitable[None]
]


class DeleteThreadsHook(FilterHook[DeleteThreadsAction, DeleteThreadsFilter]):
    async def call_action(
        self,
        action: DeleteThreadsAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadsInput,
    ):
        await self.filter(action, context, cleaned_data)


delete_threads_hook = DeleteThreadsHook()
delete_threads_input_hook = DeleteThreadsInputHook()
delete_threads_input_model_hook = DeleteThreadsInputModelHook()
