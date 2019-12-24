from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    CloseThreadsAction,
    CloseThreadsFilter,
    CloseThreadsInput,
    CloseThreadsInputAction,
    CloseThreadsInputFilter,
    CloseThreadsInputModel,
    CloseThreadsInputModelAction,
    CloseThreadsInputModelFilter,
    Thread,
)
from .filter import FilterHook


class CloseThreadsHook(FilterHook[CloseThreadsAction, CloseThreadsFilter]):
    async def call_action(
        self,
        action: CloseThreadsAction,
        context: GraphQLContext,
        cleaned_data: CloseThreadsInput,
    ) -> List[Thread]:
        return await self.filter(action, context, cleaned_data)


class CloseThreadsInputHook(
    FilterHook[CloseThreadsInputAction, CloseThreadsInputFilter]
):
    async def call_action(
        self,
        action: CloseThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: CloseThreadsInput,
        errors_list: ErrorsList,
    ) -> Tuple[CloseThreadsInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class CloseThreadsInputModelHook(
    FilterHook[CloseThreadsInputModelAction, CloseThreadsInputModelFilter]
):
    async def call_action(
        self, action: CloseThreadsInputModelAction, context: GraphQLContext
    ) -> CloseThreadsInputModel:
        return await self.filter(action, context)
