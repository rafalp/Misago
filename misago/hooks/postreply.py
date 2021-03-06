from typing import Awaitable, Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    GraphQLContext,
    ParsedMarkupMetadata,
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
    Validator,
)
from .filter import FilterHook


class PostReplyHook(FilterHook[PostReplyAction, PostReplyFilter]):
    def call_action(
        self,
        action: PostReplyAction,
        context: GraphQLContext,
        cleaned_data: PostReplyInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


class PostReplyInputHook(FilterHook[PostReplyInputAction, PostReplyInputFilter]):
    def call_action(
        self,
        action: PostReplyInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: PostReplyInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostReplyInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class PostReplyInputModelHook(
    FilterHook[PostReplyInputModelAction, PostReplyInputModelFilter]
):
    def call_action(
        self, action: PostReplyInputModelAction, context: GraphQLContext
    ) -> Awaitable[PostReplyInputModel]:
        return self.filter(action, context)
