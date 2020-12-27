from typing import Awaitable, Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadAction,
    DeleteThreadFilter,
    DeleteThreadInput,
    DeleteThreadInputAction,
    DeleteThreadInputFilter,
    DeleteThreadInputModel,
    DeleteThreadInputModelAction,
    DeleteThreadInputModelFilter,
)
from .filter import FilterHook


class DeleteThreadHook(FilterHook[DeleteThreadAction, DeleteThreadFilter]):
    async def call_action(
        self,
        action: DeleteThreadAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadInput,
    ):
        await self.filter(action, context, cleaned_data)


class DeleteThreadInputHook(
    FilterHook[DeleteThreadInputAction, DeleteThreadInputFilter]
):
    def call_action(
        self,
        action: DeleteThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class DeleteThreadInputModelHook(
    FilterHook[DeleteThreadInputModelAction, DeleteThreadInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadInputModel]:
        return self.filter(action, context)
