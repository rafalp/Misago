from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    Post,
    PostReplyAction,
    PostReplyFilter,
    PostReplyInput,
    PostReplyInputAction,
    PostReplyInputFilter,
    PostReplyInputModel,
    PostReplyInputModelAction,
    PostReplyInputModelFilter,
    Thread,
)
from .filter import FilterHook


class PostReplyHook(FilterHook[PostReplyAction, PostReplyFilter]):
    async def call_action(
        self,
        action: PostReplyAction,
        context: GraphQLContext,
        cleaned_data: PostReplyInput,
    ) -> Tuple[Thread, Post]:
        return await self.filter(action, context, cleaned_data)


class PostReplyInputHook(FilterHook[PostReplyInputAction, PostReplyInputFilter]):
    async def call_action(
        self,
        action: PostReplyInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: PostReplyInput,
        errors_list: ErrorsList,
    ) -> Tuple[PostReplyInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class PostReplyInputModelHook(
    FilterHook[PostReplyInputModelAction, PostReplyInputModelFilter]
):
    async def call_action(
        self, action: PostReplyInputModelAction, context: GraphQLContext
    ) -> PostReplyInputModel:
        return await self.filter(action, context)
