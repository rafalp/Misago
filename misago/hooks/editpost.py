from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
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
)
from .filter import FilterHook


class EditPostHook(FilterHook[EditPostAction, EditPostFilter]):
    async def call_action(
        self,
        action: EditPostAction,
        context: GraphQLContext,
        cleaned_data: EditPostInput,
    ) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
        return await self.filter(action, context, cleaned_data)


class EditPostInputHook(FilterHook[EditPostInputAction, EditPostInputFilter]):
    async def call_action(
        self,
        action: EditPostInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: EditPostInput,
        errors_list: ErrorsList,
    ) -> Tuple[EditPostInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class EditPostInputModelHook(
    FilterHook[EditPostInputModelAction, EditPostInputModelFilter]
):
    async def call_action(
        self, action: EditPostInputModelAction, context: GraphQLContext
    ) -> EditPostInputModel:
        return await self.filter(action, context)
