from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadRepliesAction,
    DeleteThreadRepliesFilter,
    DeleteThreadRepliesInput,
    DeleteThreadRepliesInputModel,
    DeleteThreadRepliesInputModelAction,
    DeleteThreadRepliesInputModelFilter,
    DeleteThreadRepliesInputRepliesAction,
    DeleteThreadRepliesInputRepliesFilter,
    DeleteThreadRepliesInputThreadAction,
    DeleteThreadRepliesInputThreadFilter,
    Thread,
)
from .filter import FilterHook


class DeleteThreadRepliesHook(
    FilterHook[DeleteThreadRepliesAction, DeleteThreadRepliesFilter]
):
    async def call_action(
        self,
        action: DeleteThreadRepliesAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadRepliesInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class DeleteThreadRepliesInputRepliesHook(
    FilterHook[
        DeleteThreadRepliesInputRepliesAction, DeleteThreadRepliesInputRepliesFilter
    ]
):
    async def call_action(
        self,
        action: DeleteThreadRepliesInputRepliesAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadRepliesInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadRepliesInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadRepliesInputThreadHook(
    FilterHook[
        DeleteThreadRepliesInputThreadAction, DeleteThreadRepliesInputThreadFilter
    ]
):
    async def call_action(
        self,
        action: DeleteThreadRepliesInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadRepliesInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadRepliesInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadRepliesInputModelHook(
    FilterHook[DeleteThreadRepliesInputModelAction, DeleteThreadRepliesInputModelFilter]
):
    async def call_action(
        self, action: DeleteThreadRepliesInputModelAction, context: GraphQLContext
    ) -> DeleteThreadRepliesInputModel:
        return await self.filter(action, context)
