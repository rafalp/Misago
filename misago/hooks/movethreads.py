from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    MoveThreadsAction,
    MoveThreadsFilter,
    MoveThreadsInput,
    MoveThreadsInputAction,
    MoveThreadsInputFilter,
    MoveThreadsInputModel,
    MoveThreadsInputModelAction,
    MoveThreadsInputModelFilter,
    Thread,
)
from .filter import FilterHook


class MoveThreadsHook(FilterHook[MoveThreadsAction, MoveThreadsFilter]):
    async def call_action(
        self,
        action: MoveThreadsAction,
        context: GraphQLContext,
        cleaned_data: MoveThreadsInput,
    ) -> List[Thread]:
        return await self.filter(action, context, cleaned_data)


class MoveThreadsInputHook(FilterHook[MoveThreadsInputAction, MoveThreadsInputFilter]):
    async def call_action(
        self,
        action: MoveThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: MoveThreadsInput,
        errors_list: ErrorsList,
    ) -> Tuple[MoveThreadsInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class MoveThreadsInputModelHook(
    FilterHook[MoveThreadsInputModelAction, MoveThreadsInputModelFilter]
):
    async def call_action(
        self, action: MoveThreadsInputModelAction, context: GraphQLContext
    ) -> MoveThreadsInputModel:
        return await self.filter(action, context)
