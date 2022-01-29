from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import ErrorsList, Validator
from .... import GraphQLContext

PostDeleteInput = Dict[str, Any]
PostDeleteInputThreadAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostDeleteInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostDeleteInput, ErrorsList]],
]
PostDeleteInputThreadFilter = Callable[
    [PostDeleteInputThreadAction, GraphQLContext, PostDeleteInput],
    Awaitable[Tuple[PostDeleteInput, ErrorsList]],
]


class PostDeleteInputThreadHook(
    FilterHook[PostDeleteInputThreadAction, PostDeleteInputThreadFilter]
):
    def call_action(
        self,
        action: PostDeleteInputThreadAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: PostDeleteInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostDeleteInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


PostDeleteInputPostAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostDeleteInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostDeleteInput, ErrorsList]],
]
PostDeleteInputPostFilter = Callable[
    [PostDeleteInputPostAction, GraphQLContext, PostDeleteInput],
    Awaitable[Tuple[PostDeleteInput, ErrorsList]],
]


class PostDeleteInputPostHook(
    FilterHook[PostDeleteInputPostAction, PostDeleteInputPostFilter]
):
    def call_action(
        self,
        action: PostDeleteInputPostAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: PostDeleteInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostDeleteInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


PostDeleteAction = Callable[[GraphQLContext, PostDeleteInput], Awaitable[Thread]]
PostDeleteFilter = Callable[
    [PostDeleteAction, GraphQLContext, PostDeleteInput], Awaitable[Thread]
]


class PostDeleteHook(FilterHook[PostDeleteAction, PostDeleteFilter]):
    def call_action(
        self,
        action: PostDeleteAction,
        context: GraphQLContext,
        cleaned_data: PostDeleteInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


post_delete_hook = PostDeleteHook()
post_delete_input_post_hook = PostDeleteInputPostHook()
post_delete_input_thread_hook = PostDeleteInputThreadHook()
