from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    MoveThreadAction,
    MoveThreadFilter,
    MoveThreadInput,
    MoveThreadInputAction,
    MoveThreadInputFilter,
    MoveThreadInputModel,
    MoveThreadInputModelAction,
    MoveThreadInputModelFilter,
    Thread,
)
from .filter import FilterHook


class MoveThreadHook(FilterHook[MoveThreadAction, MoveThreadFilter]):
    async def call_action(
        self,
        action: MoveThreadAction,
        context: GraphQLContext,
        cleaned_data: MoveThreadInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class MoveThreadInputHook(FilterHook[MoveThreadInputAction, MoveThreadInputFilter]):
    async def call_action(
        self,
        action: MoveThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: MoveThreadInput,
        errors_list: ErrorsList,
    ) -> Tuple[MoveThreadInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class MoveThreadInputModelHook(
    FilterHook[MoveThreadInputModelAction, MoveThreadInputModelFilter]
):
    async def call_action(
        self, action: MoveThreadInputModelAction, context: GraphQLContext
    ) -> MoveThreadInputModel:
        return await self.filter(action, context)
