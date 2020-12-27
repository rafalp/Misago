from typing import Awaitable, Dict, List, Tuple

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
    def call_action(
        self,
        action: MoveThreadAction,
        context: GraphQLContext,
        cleaned_data: MoveThreadInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


class MoveThreadInputHook(FilterHook[MoveThreadInputAction, MoveThreadInputFilter]):
    def call_action(
        self,
        action: MoveThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: MoveThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[MoveThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class MoveThreadInputModelHook(
    FilterHook[MoveThreadInputModelAction, MoveThreadInputModelFilter]
):
    def call_action(
        self, action: MoveThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[MoveThreadInputModel]:
        return self.filter(action, context)
