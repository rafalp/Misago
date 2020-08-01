from typing import Dict, List, Tuple

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
    async def call_action(
        self,
        action: DeleteThreadPostsAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadPostsInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class DeleteThreadPostsInputPostsHook(
    FilterHook[DeleteThreadPostsInputPostsAction, DeleteThreadPostsInputPostsFilter]
):
    async def call_action(
        self,
        action: DeleteThreadPostsInputPostsAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadPostsInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadPostsInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostsInputThreadHook(
    FilterHook[DeleteThreadPostsInputThreadAction, DeleteThreadPostsInputThreadFilter]
):
    async def call_action(
        self,
        action: DeleteThreadPostsInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadPostsInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadPostsInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostsInputModelHook(
    FilterHook[DeleteThreadPostsInputModelAction, DeleteThreadPostsInputModelFilter]
):
    async def call_action(
        self, action: DeleteThreadPostsInputModelAction, context: GraphQLContext
    ) -> DeleteThreadPostsInputModel:
        return await self.filter(action, context)
