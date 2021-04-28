from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....richtext import ParsedMarkupMetadata
from .....threads.models import Post, Thread
from .....types import Validator
from .... import GraphQLContext

PostThreadInputModel = Type[BaseModel]
PostThreadInputModelAction = Callable[[GraphQLContext], Awaitable[PostThreadInputModel]]
PostThreadInputModelFilter = Callable[
    [PostThreadInputModelAction, GraphQLContext],
    Awaitable[PostThreadInputModel],
]


class PostThreadInputModelHook(
    FilterHook[PostThreadInputModelAction, PostThreadInputModelFilter]
):
    def call_action(
        self, action: PostThreadInputModelAction, context: GraphQLContext
    ) -> Awaitable[PostThreadInputModel]:
        return self.filter(action, context)


PostThreadInput = Dict[str, Any]
PostThreadInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostThreadInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostThreadInput, ErrorsList]],
]
PostThreadInputFilter = Callable[
    [PostThreadInputAction, GraphQLContext, PostThreadInput],
    Awaitable[Tuple[PostThreadInput, ErrorsList]],
]


class PostThreadInputHook(FilterHook[PostThreadInputAction, PostThreadInputFilter]):
    def call_action(
        self,
        action: PostThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: PostThreadInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostThreadInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


PostThreadAction = Callable[
    [GraphQLContext, PostThreadInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
PostThreadFilter = Callable[
    [PostThreadAction, GraphQLContext, PostThreadInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]


class PostThreadHook(FilterHook[PostThreadAction, PostThreadFilter]):
    def call_action(
        self,
        action: PostThreadAction,
        context: GraphQLContext,
        cleaned_data: PostThreadInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


post_thread_hook = PostThreadHook()
post_thread_input_hook = PostThreadInputHook()
post_thread_input_model_hook = PostThreadInputModelHook()
