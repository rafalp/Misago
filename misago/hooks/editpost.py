from typing import Awaitable, Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    EditPostAction,
    EditPostFilter,
    EditPostInput,
    EditPostInputAction,
    EditPostInputFilter,
    EditPostInputModel,
    EditPostInputModelAction,
    EditPostInputModelFilter,
    GraphQLContext,
    ParsedMarkupMetadata,
    Post,
    Thread,
    Validator,
)
from .filter import FilterHook


class EditPostHook(FilterHook[EditPostAction, EditPostFilter]):
    def call_action(
        self,
        action: EditPostAction,
        context: GraphQLContext,
        cleaned_data: EditPostInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


class EditPostInputHook(FilterHook[EditPostInputAction, EditPostInputFilter]):
    def call_action(
        self,
        action: EditPostInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: EditPostInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[EditPostInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class EditPostInputModelHook(
    FilterHook[EditPostInputModelAction, EditPostInputModelFilter]
):
    def call_action(
        self, action: EditPostInputModelAction, context: GraphQLContext
    ) -> Awaitable[EditPostInputModel]:
        return self.filter(action, context)
