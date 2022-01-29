from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import ErrorsList, Validator
from .... import GraphQLContext

PostsBulkDeleteInput = Dict[str, Any]
PostsBulkDeleteInputThreadAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostsBulkDeleteInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostsBulkDeleteInput, ErrorsList]],
]
PostsBulkDeleteInputThreadFilter = Callable[
    [PostsBulkDeleteInputThreadAction, GraphQLContext, PostsBulkDeleteInput],
    Awaitable[Tuple[PostsBulkDeleteInput, ErrorsList]],
]


class PostsBulkDeleteInputThreadHook(
    FilterHook[PostsBulkDeleteInputThreadAction, PostsBulkDeleteInputThreadFilter]
):
    def call_action(
        self,
        action: PostsBulkDeleteInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: PostsBulkDeleteInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostsBulkDeleteInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


PostsBulkDeleteInputPostsAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostsBulkDeleteInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostsBulkDeleteInput, ErrorsList]],
]
PostsBulkDeleteInputPostsFilter = Callable[
    [PostsBulkDeleteInputPostsAction, GraphQLContext, PostsBulkDeleteInput],
    Awaitable[Tuple[PostsBulkDeleteInput, ErrorsList]],
]


class PostsBulkDeleteInputPostsHook(
    FilterHook[PostsBulkDeleteInputPostsAction, PostsBulkDeleteInputPostsFilter]
):
    def call_action(
        self,
        action: PostsBulkDeleteInputPostsAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: PostsBulkDeleteInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostsBulkDeleteInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


PostsBulkDeleteAction = Callable[
    [GraphQLContext, PostsBulkDeleteInput], Awaitable[Thread]
]
PostsBulkDeleteFilter = Callable[
    [PostsBulkDeleteAction, GraphQLContext, PostsBulkDeleteInput],
    Awaitable[Thread],
]


class PostsBulkDeleteHook(FilterHook[PostsBulkDeleteAction, PostsBulkDeleteFilter]):
    def call_action(
        self,
        action: PostsBulkDeleteAction,
        context: GraphQLContext,
        cleaned_data: PostsBulkDeleteInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


posts_bulk_delete_hook = PostsBulkDeleteHook()
posts_bulk_delete_input_posts_hook = PostsBulkDeleteInputPostsHook()
posts_bulk_delete_input_thread_hook = PostsBulkDeleteInputThreadHook()
