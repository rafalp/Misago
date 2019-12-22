from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    EditThreadTitleAction,
    EditThreadTitleFilter,
    EditThreadTitleInput,
    EditThreadTitleInputAction,
    EditThreadTitleInputFilter,
    EditThreadTitleInputModel,
    EditThreadTitleInputModelAction,
    EditThreadTitleInputModelFilter,
    Thread,
)
from .filter import FilterHook


class EditThreadTitleHook(FilterHook[EditThreadTitleAction, EditThreadTitleFilter]):
    async def call_action(
        self,
        action: EditThreadTitleAction,
        context: GraphQLContext,
        cleaned_data: EditThreadTitleInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class EditThreadTitleInputHook(
    FilterHook[EditThreadTitleInputAction, EditThreadTitleInputFilter]
):
    async def call_action(
        self,
        action: EditThreadTitleInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: EditThreadTitleInput,
        errors_list: ErrorsList,
    ) -> Tuple[EditThreadTitleInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class EditThreadTitleInputModelHook(
    FilterHook[EditThreadTitleInputModelAction, EditThreadTitleInputModelFilter]
):
    async def call_action(
        self, action: EditThreadTitleInputModelAction, context: GraphQLContext
    ) -> EditThreadTitleInputModel:
        return await self.filter(action, context)
