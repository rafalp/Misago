from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from ..types import GraphQLContext, Thread, Validator
from .filter import FilterHook

DeleteThreadPostsInputModel = Type[BaseModel]
DeleteThreadPostsInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadPostsInputModel]
]
DeleteThreadPostsInputModelFilter = Callable[
    [DeleteThreadPostsInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadPostsInputModel],
]


class DeleteThreadPostsInputModelHook(
    FilterHook[DeleteThreadPostsInputModelAction, DeleteThreadPostsInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadPostsInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadPostsInputModel]:
        return self.filter(action, context)


DeleteThreadPostsInput = Dict[str, Any]
DeleteThreadPostsInputThreadAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        DeleteThreadPostsInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]
DeleteThreadPostsInputThreadFilter = Callable[
    [DeleteThreadPostsInputThreadAction, GraphQLContext, DeleteThreadPostsInput],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]


class DeleteThreadPostsInputThreadHook(
    FilterHook[DeleteThreadPostsInputThreadAction, DeleteThreadPostsInputThreadFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostsInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadPostsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


DeleteThreadPostsInputPostsAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        DeleteThreadPostsInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]
DeleteThreadPostsInputPostsFilter = Callable[
    [DeleteThreadPostsInputPostsAction, GraphQLContext, DeleteThreadPostsInput],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]


class DeleteThreadPostsInputPostsHook(
    FilterHook[DeleteThreadPostsInputPostsAction, DeleteThreadPostsInputPostsFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostsInputPostsAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadPostsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


DeleteThreadPostsAction = Callable[
    [GraphQLContext, DeleteThreadPostsInput], Awaitable[Thread]
]
DeleteThreadPostsFilter = Callable[
    [DeleteThreadPostsAction, GraphQLContext, DeleteThreadPostsInput],
    Awaitable[Thread],
]


class DeleteThreadPostsHook(
    FilterHook[DeleteThreadPostsAction, DeleteThreadPostsFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostsAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadPostsInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


delete_thread_posts_hook = DeleteThreadPostsHook()
delete_thread_posts_input_model_hook = DeleteThreadPostsInputModelHook()
delete_thread_posts_input_posts_hook = DeleteThreadPostsInputPostsHook()
delete_thread_posts_input_thread_hook = DeleteThreadPostsInputThreadHook()
