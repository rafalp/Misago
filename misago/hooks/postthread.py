from typing import Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    ParsedMarkupMetadata,
    Post,
    PostThreadAction,
    PostThreadFilter,
    PostThreadInput,
    PostThreadInputAction,
    PostThreadInputFilter,
    PostThreadInputModel,
    PostThreadInputModelAction,
    PostThreadInputModelFilter,
    Thread,
)
from .filter import FilterHook


class PostThreadHook(FilterHook[PostThreadAction, PostThreadFilter]):
    async def call_action(
        self,
        action: PostThreadAction,
        context: GraphQLContext,
        cleaned_data: PostThreadInput,
    ) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
        return await self.filter(action, context, cleaned_data)


class PostThreadInputHook(FilterHook[PostThreadInputAction, PostThreadInputFilter]):
    async def call_action(
        self,
        action: PostThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: PostThreadInput,
        errors_list: ErrorsList,
    ) -> Tuple[PostThreadInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class PostThreadInputModelHook(
    FilterHook[PostThreadInputModelAction, PostThreadInputModelFilter]
):
    async def call_action(
        self, action: PostThreadInputModelAction, context: GraphQLContext
    ) -> PostThreadInputModel:
        return await self.filter(action, context)
