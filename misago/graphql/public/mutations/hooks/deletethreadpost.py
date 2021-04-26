from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....types import GraphQLContext, Thread, Validator

DeleteThreadPostInputModel = Type[BaseModel]
DeleteThreadPostInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadPostInputModel]
]
DeleteThreadPostInputModelFilter = Callable[
    [DeleteThreadPostInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadPostInputModel],
]


class DeleteThreadPostInputModelHook(
    FilterHook[DeleteThreadPostInputModelAction, DeleteThreadPostInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadPostInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadPostInputModel]:
        return self.filter(action, context)


DeleteThreadPostInput = Dict[str, Any]
DeleteThreadPostInputThreadAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        DeleteThreadPostInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]
DeleteThreadPostInputThreadFilter = Callable[
    [DeleteThreadPostInputThreadAction, GraphQLContext, DeleteThreadPostInput],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]


class DeleteThreadPostInputThreadHook(
    FilterHook[DeleteThreadPostInputThreadAction, DeleteThreadPostInputThreadFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadPostInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


DeleteThreadPostInputPostAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        DeleteThreadPostInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]
DeleteThreadPostInputPostFilter = Callable[
    [DeleteThreadPostInputPostAction, GraphQLContext, DeleteThreadPostInput],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]


class DeleteThreadPostInputPostHook(
    FilterHook[DeleteThreadPostInputPostAction, DeleteThreadPostInputPostFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostInputPostAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadPostInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


DeleteThreadPostAction = Callable[
    [GraphQLContext, DeleteThreadPostInput], Awaitable[Thread]
]
DeleteThreadPostFilter = Callable[
    [DeleteThreadPostAction, GraphQLContext, DeleteThreadPostInput], Awaitable[Thread]
]


class DeleteThreadPostHook(FilterHook[DeleteThreadPostAction, DeleteThreadPostFilter]):
    def call_action(
        self,
        action: DeleteThreadPostAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadPostInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


delete_thread_post_hook = DeleteThreadPostHook()
delete_thread_post_input_model_hook = DeleteThreadPostInputModelHook()
delete_thread_post_input_post_hook = DeleteThreadPostInputPostHook()
delete_thread_post_input_thread_hook = DeleteThreadPostInputThreadHook()
