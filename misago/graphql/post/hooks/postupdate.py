from typing import Any, Awaitable, Callable, Dict, List, Tuple

from ....context import Context
from ....hooks import FilterHook
from ....richtext import ParsedMarkupMetadata
from ....threads.models import Post, Thread
from ....validation import ErrorsList, Validator

PostUpdateInput = Dict[str, Any]
PostUpdateInputAction = Callable[
    [
        Context,
        Dict[str, List[Validator]],
        PostUpdateInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostUpdateInput, ErrorsList]],
]
PostUpdateInputFilter = Callable[
    [PostUpdateInputAction, Context, PostUpdateInput],
    Awaitable[Tuple[PostUpdateInput, ErrorsList]],
]


class PostUpdateInputHook(FilterHook[PostUpdateInputAction, PostUpdateInputFilter]):
    def call_action(
        self,
        action: PostUpdateInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: PostUpdateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[PostUpdateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


PostUpdateAction = Callable[
    [Context, PostUpdateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
PostUpdateFilter = Callable[
    [PostUpdateAction, Context, PostUpdateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]


class PostUpdateHook(FilterHook[PostUpdateAction, PostUpdateFilter]):
    def call_action(
        self,
        action: PostUpdateAction,
        context: Context,
        cleaned_data: PostUpdateInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


post_update_hook = PostUpdateHook()
post_update_input_hook = PostUpdateInputHook()
