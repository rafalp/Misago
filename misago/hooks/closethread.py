from typing import Awaitable, Dict, List, Tuple

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
    def call_action(
        self,
        action: CloseThreadAction,
        context: GraphQLContext,
        cleaned_data: CloseThreadInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


class CloseThreadInputHook(FilterHook[CloseThreadInputAction, CloseThreadInputFilter]):
    def call_action(
        self,
        action: CloseThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: CloseThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[CloseThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class CloseThreadInputModelHook(
    FilterHook[CloseThreadInputModelAction, CloseThreadInputModelFilter]
):
    def call_action(
        self, action: CloseThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[CloseThreadInputModel]:
        return self.filter(action, context)
