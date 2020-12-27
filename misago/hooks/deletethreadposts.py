from typing import Awaitable, Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadPostsAction,
    DeleteThreadPostsFilter,
    DeleteThreadPostsInput,
    DeleteThreadPostsInputModel,
    DeleteThreadPostsInputModelAction,
    DeleteThreadPostsInputModelFilter,
    DeleteThreadPostsInputPostsAction,
    DeleteThreadPostsInputPostsFilter,
    DeleteThreadPostsInputThreadAction,
    DeleteThreadPostsInputThreadFilter,
    Thread,
)
from .filter import FilterHook


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


class DeleteThreadPostsInputPostsHook(
    FilterHook[DeleteThreadPostsInputPostsAction, DeleteThreadPostsInputPostsFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostsInputPostsAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadPostsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostsInputThreadHook(
    FilterHook[DeleteThreadPostsInputThreadAction, DeleteThreadPostsInputThreadFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostsInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadPostsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostsInputModelHook(
    FilterHook[DeleteThreadPostsInputModelAction, DeleteThreadPostsInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadPostsInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadPostsInputModel]:
        return self.filter(action, context)
