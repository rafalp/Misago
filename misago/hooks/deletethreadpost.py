from typing import Awaitable, Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    DeleteThreadPostAction,
    DeleteThreadPostFilter,
    DeleteThreadPostInput,
    DeleteThreadPostInputModel,
    DeleteThreadPostInputModelAction,
    DeleteThreadPostInputModelFilter,
    DeleteThreadPostInputPostAction,
    DeleteThreadPostInputPostFilter,
    DeleteThreadPostInputThreadAction,
    DeleteThreadPostInputThreadFilter,
    GraphQLContext,
    Thread,
    Validator,
)
from .filter import FilterHook


class DeleteThreadPostHook(FilterHook[DeleteThreadPostAction, DeleteThreadPostFilter]):
    def call_action(
        self,
        action: DeleteThreadPostAction,
        context: GraphQLContext,
        cleaned_data: DeleteThreadPostInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


class DeleteThreadPostInputPostHook(
    FilterHook[DeleteThreadPostInputPostAction, DeleteThreadPostInputPostFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostInputPostAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadPostInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostInputThreadHook(
    FilterHook[DeleteThreadPostInputThreadAction, DeleteThreadPostInputThreadFilter]
):
    def call_action(
        self,
        action: DeleteThreadPostInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: DeleteThreadPostInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class DeleteThreadPostInputModelHook(
    FilterHook[DeleteThreadPostInputModelAction, DeleteThreadPostInputModelFilter]
):
    def call_action(
        self, action: DeleteThreadPostInputModelAction, context: GraphQLContext
    ) -> Awaitable[DeleteThreadPostInputModel]:
        return self.filter(action, context)
