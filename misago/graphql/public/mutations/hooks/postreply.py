from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....types import (
    GraphQLContext,
    ParsedMarkupMetadata,
    Post,
    Thread,
    Validator,
)

PostReplyInputModel = Type[BaseModel]
PostReplyInputModelAction = Callable[[GraphQLContext], Awaitable[PostReplyInputModel]]
PostReplyInputModelFilter = Callable[
    [PostReplyInputModelAction, GraphQLContext],
    Awaitable[PostReplyInputModel],
]


class PostReplyInputModelHook(
    FilterHook[PostReplyInputModelAction, PostReplyInputModelFilter]
):
    def call_action(
        self, action: PostReplyInputModelAction, context: GraphQLContext
    ) -> Awaitable[PostReplyInputModel]:
        return self.filter(action, context)


PostReplyInput = Dict[str, Any]
PostReplyInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostReplyInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostReplyInput, ErrorsList]],
]
PostReplyInputFilter = Callable[
    [PostReplyInputAction, GraphQLContext, PostReplyInput],
    Awaitable[Tuple[PostReplyInput, ErrorsList]],
]


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


PostReplyAction = Callable[
    [GraphQLContext, PostReplyInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
PostReplyFilter = Callable[
    [PostReplyAction, GraphQLContext, PostReplyInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]


class PostReplyHook(FilterHook[PostReplyAction, PostReplyFilter]):
    def call_action(
        self,
        action: PostReplyAction,
        context: GraphQLContext,
        cleaned_data: PostReplyInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


post_reply_hook = PostReplyHook()
post_reply_input_hook = PostReplyInputHook()
post_reply_input_model_hook = PostReplyInputModelHook()
