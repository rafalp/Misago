from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadPostAction,
    DeleteThreadPostFilter,
    DeleteThreadPostInput,
    DeleteThreadPostInputModel,
    DeleteThreadPostInputModelAction,
    DeleteThreadPostInputModelFilter,
    DeleteThreadPostInputPostAction,
    DeleteThreadPostInputPostFilter,
    DeleteThreadPostInputThreadAction,
    DeleteThreadPostInputThreadFilter,
    Thread,
)
from .filter import FilterHook


class DeleteThreadPostHook(FilterHook[DeleteThreadPostAction, DeleteThreadPostFilter]):
    async def call_action(
        self,
        action: DeleteThreadPostAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadPostInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class DeleteThreadPostInputPostHook(
    FilterHook[DeleteThreadPostInputPostAction, DeleteThreadPostInputPostFilter]
):
    async def call_action(
        self,
        action: DeleteThreadPostInputPostAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadPostInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadPostInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostInputThreadHook(
    FilterHook[DeleteThreadPostInputThreadAction, DeleteThreadPostInputThreadFilter]
):
    async def call_action(
        self,
        action: DeleteThreadPostInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadPostInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadPostInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostInputModelHook(
    FilterHook[DeleteThreadPostInputModelAction, DeleteThreadPostInputModelFilter]
):
    async def call_action(
        self, action: DeleteThreadPostInputModelAction, context: GraphQLContext
    ) -> DeleteThreadPostInputModel:
        return await self.filter(action, context)
