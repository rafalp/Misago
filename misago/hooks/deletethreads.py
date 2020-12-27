from typing import Awaitable, Dict, List, Tuple

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
    def call_action(
        self,
        action: DeleteThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: DeleteThreadsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class DeleteThreadsInputModelHook(
    FilterHook[DeleteThreadsInputModelAction, DeleteThreadsInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadsInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadsInputModel]:
        return self.filter(action, context)
