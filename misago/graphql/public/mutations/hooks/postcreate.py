from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....richtext import ParsedMarkupMetadata
from .....threads.models import Post, Thread
from .....validation import Validator
from .... import GraphQLContext

PostCreateInputModel = Type[BaseModel]
PostCreateInputModelAction = Callable[[GraphQLContext], Awaitable[PostCreateInputModel]]
PostCreateInputModelFilter = Callable[
    [PostCreateInputModelAction, GraphQLContext],
    Awaitable[PostCreateInputModel],
]


class PostCreateInputModelHook(
    FilterHook[PostCreateInputModelAction, PostCreateInputModelFilter]
):
    def call_action(
        self, action: PostCreateInputModelAction, context: GraphQLContext
    ) -> Awaitable[PostCreateInputModel]:
        return self.filter(action, context)


PostCreateInput = Dict[str, Any]
PostCreateInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostCreateInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostCreateInput, ErrorsList]],
]
PostCreateInputFilter = Callable[
    [PostCreateInputAction, GraphQLContext, PostCreateInput],
    Awaitable[Tuple[PostCreateInput, ErrorsList]],
]


class PostCreateInputHook(FilterHook[PostCreateInputAction, PostCreateInputFilter]):
    def call_action(
        self,
        action: PostCreateInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: PostCreateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostCreateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


PostCreateAction = Callable[
    [GraphQLContext, PostCreateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
PostCreateFilter = Callable[
    [PostCreateAction, GraphQLContext, PostCreateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]


class PostCreateHook(FilterHook[PostCreateAction, PostCreateFilter]):
    def call_action(
        self,
        action: PostCreateAction,
        context: GraphQLContext,
        cleaned_data: PostCreateInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


post_create_hook = PostCreateHook()
post_create_input_hook = PostCreateInputHook()
post_create_input_model_hook = PostCreateInputModelHook()
