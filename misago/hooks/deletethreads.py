from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadsAction,
    DeleteThreadsFilter,
    DeleteThreadsInput,
    DeleteThreadsInputAction,
    DeleteThreadsInputFilter,
    DeleteThreadsInputModel,
    DeleteThreadsInputModelAction,
    DeleteThreadsInputModelFilter,
)
from .filter import FilterHook


class DeleteThreadsHook(FilterHook[DeleteThreadsAction, DeleteThreadsFilter]):
    async def call_action(
        self,
        action: DeleteThreadsAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadsInput,
    ):
        await self.filter(action, context, cleaned_data)


class DeleteThreadsInputHook(
    FilterHook[DeleteThreadsInputAction, DeleteThreadsInputFilter]
):
    async def call_action(
        self,
        action: DeleteThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadsInput,
        errors_list: ErrorsList,
    ) -> Tuple[DeleteThreadsInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class DeleteThreadsInputModelHook(
    FilterHook[DeleteThreadsInputModelAction, DeleteThreadsInputModelFilter]
):
    async def call_action(
        self, action: DeleteThreadsInputModelAction, context: GraphQLContext
    ) -> DeleteThreadsInputModel:
        return await self.filter(action, context)
