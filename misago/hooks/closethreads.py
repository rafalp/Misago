from typing import Awaitable, Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    CloseThreadsAction,
    CloseThreadsFilter,
    CloseThreadsInput,
    CloseThreadsInputAction,
    CloseThreadsInputFilter,
    CloseThreadsInputModel,
    CloseThreadsInputModelAction,
    CloseThreadsInputModelFilter,
    GraphQLContext,
    Thread,
    Validator,
)
from .filter import FilterHook


class CloseThreadsHook(FilterHook[CloseThreadsAction, CloseThreadsFilter]):
    def call_action(
        self,
        action: CloseThreadsAction,
        context: GraphQLContext,
        cleaned_data: CloseThreadsInput,
    ) -> Awaitable[List[Thread]]:
        return self.filter(action, context, cleaned_data)


class CloseThreadsInputHook(
    FilterHook[CloseThreadsInputAction, CloseThreadsInputFilter]
):
    def call_action(
        self,
        action: CloseThreadsInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: CloseThreadsInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[CloseThreadsInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class CloseThreadsInputModelHook(
    FilterHook[CloseThreadsInputModelAction, CloseThreadsInputModelFilter]
):
    def call_action(
        self, action: CloseThreadsInputModelAction, context: GraphQLContext
    ) -> Awaitable[CloseThreadsInputModel]:
        return self.filter(action, context)
