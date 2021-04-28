from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....types import Validator
from .... import GraphQLContext

DeleteThreadInputModel = Type[BaseModel]
DeleteThreadInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadInputModel]
]
DeleteThreadInputModelFilter = Callable[
    [DeleteThreadInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadInputModel],
]


class DeleteThreadInputModelHook(
    FilterHook[DeleteThreadInputModelAction, DeleteThreadInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadInputModel]:
        return self.filter(action, context)


DeleteThreadInput = Dict[str, Any]
DeleteThreadInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], DeleteThreadInput, ErrorsList],
    Awaitable[Tuple[DeleteThreadInput, ErrorsList]],
]
DeleteThreadInputFilter = Callable[
    [DeleteThreadInputAction, GraphQLContext, DeleteThreadInput],
    Awaitable[Tuple[DeleteThreadInput, ErrorsList]],
]


class DeleteThreadInputHook(
    FilterHook[DeleteThreadInputAction, DeleteThreadInputFilter]
):
    def call_action(
        self,
        action: DeleteThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


DeleteThreadAction = Callable[[GraphQLContext, DeleteThreadInput], Awaitable[None]]
DeleteThreadFilter = Callable[
    [DeleteThreadAction, GraphQLContext, DeleteThreadInput], Awaitable[None]
]


class DeleteThreadHook(FilterHook[DeleteThreadAction, DeleteThreadFilter]):
    async def call_action(
        self,
        action: DeleteThreadAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadInput,
    ):
        await self.filter(action, context, cleaned_data)


delete_thread_hook = DeleteThreadHook()
delete_thread_input_hook = DeleteThreadInputHook()
delete_thread_input_model_hook = DeleteThreadInputModelHook()
