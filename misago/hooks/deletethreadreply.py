from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadReplyAction,
    DeleteThreadReplyFilter,
    DeleteThreadReplyInput,
    DeleteThreadReplyInputModel,
    DeleteThreadReplyInputModelAction,
    DeleteThreadReplyInputModelFilter,
    DeleteThreadReplyInputReplyAction,
    DeleteThreadReplyInputReplyFilter,
    DeleteThreadReplyInputThreadAction,
    DeleteThreadReplyInputThreadFilter,
    Thread,
)
from .filter import FilterHook


class DeleteThreadReplyHook(
    FilterHook[DeleteThreadReplyAction, DeleteThreadReplyFilter]
):
    async def call_action(
        self,
        action: DeleteThreadReplyAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadReplyInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class DeleteThreadReplyInputReplyHook(
    FilterHook[DeleteThreadReplyInputReplyAction, DeleteThreadReplyInputReplyFilter]
):
    async def call_action(
        self,
        action: DeleteThreadReplyInputReplyAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadReplyInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadReplyInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadReplyInputThreadHook(
    FilterHook[DeleteThreadReplyInputThreadAction, DeleteThreadReplyInputThreadFilter]
):
    async def call_action(
        self,
        action: DeleteThreadReplyInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadReplyInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadReplyInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadReplyInputModelHook(
    FilterHook[DeleteThreadReplyInputModelAction, DeleteThreadReplyInputModelFilter]
):
    async def call_action(
        self, action: DeleteThreadReplyInputModelAction, context: GraphQLContext
    ) -> DeleteThreadReplyInputModel:
        return await self.filter(action, context)
