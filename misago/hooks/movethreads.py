from typing import Awaitable, Dict, List, Tuple

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
    def call_action(
        self,
        action: MoveThreadsAction,
        context: GraphQLContext,
        cleaned_data: MoveThreadsInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


class MoveThreadsInputHook(FilterHook[MoveThreadsInputAction, MoveThreadsInputFilter]):
    def call_action(
        self,
        action: MoveThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: MoveThreadsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[MoveThreadsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class MoveThreadsInputModelHook(
    FilterHook[MoveThreadsInputModelAction, MoveThreadsInputModelFilter]
):
    def call_action(
        self, action: MoveThreadsInputModelAction, context: GraphQLContext
    ) -> Awaitable[MoveThreadsInputModel]:
        return self.filter(action, context)
