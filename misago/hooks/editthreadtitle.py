from typing import Awaitable, Dict, List, Tuple

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
    def call_action(
        self,
        action: EditThreadTitleAction,
        context: GraphQLContext,
        cleaned_data: EditThreadTitleInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


class EditThreadTitleInputHook(
    FilterHook[EditThreadTitleInputAction, EditThreadTitleInputFilter]
):
    def call_action(
        self,
        action: EditThreadTitleInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: EditThreadTitleInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[EditThreadTitleInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class EditThreadTitleInputModelHook(
    FilterHook[EditThreadTitleInputModelAction, EditThreadTitleInputModelFilter]
):
    def call_action(
        self, action: EditThreadTitleInputModelAction, context: GraphQLContext
    ) -> Awaitable[EditThreadTitleInputModel]:
        return self.filter(action, context)
