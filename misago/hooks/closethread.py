from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    CloseThreadAction,
    CloseThreadFilter,
    CloseThreadInput,
    CloseThreadInputAction,
    CloseThreadInputFilter,
    CloseThreadInputModel,
    CloseThreadInputModelAction,
    CloseThreadInputModelFilter,
    Thread,
)
from .filter import FilterHook


class CloseThreadHook(FilterHook[CloseThreadAction, CloseThreadFilter]):
    async def call_action(
        self,
        action: CloseThreadAction,
        context: GraphQLContext,
        cleaned_data: CloseThreadInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class CloseThreadInputHook(FilterHook[CloseThreadInputAction, CloseThreadInputFilter]):
    async def call_action(
        self,
        action: CloseThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: CloseThreadInput,
        errors_list: ErrorsList,
    ) -> Tuple[CloseThreadInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class CloseThreadInputModelHook(
    FilterHook[CloseThreadInputModelAction, CloseThreadInputModelFilter]
):
    async def call_action(
        self, action: CloseThreadInputModelAction, context: GraphQLContext
    ) -> CloseThreadInputModel:
        return await self.filter(action, context)
