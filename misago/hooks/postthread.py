from typing import Awaitable, Dict, List, Tuple

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
    def call_action(
        self,
        action: PostThreadAction,
        context: GraphQLContext,
        cleaned_data: PostThreadInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


class PostThreadInputHook(FilterHook[PostThreadInputAction, PostThreadInputFilter]):
    def call_action(
        self,
        action: PostThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: PostThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class PostThreadInputModelHook(
    FilterHook[PostThreadInputModelAction, PostThreadInputModelFilter]
):
    def call_action(
        self, action: PostThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[PostThreadInputModel]:
        return self.filter(action, context)
