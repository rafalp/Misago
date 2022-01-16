from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....richtext import ParsedMarkupMetadata
from .....threads.models import Post, Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadCreateInputModel = Type[BaseModel]
ThreadCreateInputModelAction = Callable[
    [GraphQLContext], Awaitable[ThreadCreateInputModel]
]
ThreadCreateInputModelFilter = Callable[
    [ThreadCreateInputModelAction, GraphQLContext],
    Awaitable[ThreadCreateInputModel],
]


class ThreadCreateInputModelHook(
    FilterHook[ThreadCreateInputModelAction, ThreadCreateInputModelFilter]
):
    def call_action(
        self, action: ThreadCreateInputModelAction, context: GraphQLContext
    ) -> Awaitable[ThreadCreateInputModel]:
        return self.filter(action, context)


ThreadCreateInput = Dict[str, Any]
ThreadCreateInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        ThreadCreateInput,
        ErrorsList,
    ],
    Awaitable[Tuple[ThreadCreateInput, ErrorsList]],
]
ThreadCreateInputFilter = Callable[
    [ThreadCreateInputAction, GraphQLContext, ThreadCreateInput],
    Awaitable[Tuple[ThreadCreateInput, ErrorsList]],
]


class ThreadCreateInputHook(
    FilterHook[ThreadCreateInputAction, ThreadCreateInputFilter]
):
    def call_action(
        self,
        action: ThreadCreateInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadCreateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadCreateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadCreateAction = Callable[
    [GraphQLContext, ThreadCreateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
ThreadCreateFilter = Callable[
    [ThreadCreateAction, GraphQLContext, ThreadCreateInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]


class ThreadCreateHook(FilterHook[ThreadCreateAction, ThreadCreateFilter]):
    def call_action(
        self,
        action: ThreadCreateAction,
        context: GraphQLContext,
        cleaned_data: ThreadCreateInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


thread_create_hook = ThreadCreateHook()
thread_create_input_hook = ThreadCreateInputHook()
thread_create_input_model_hook = ThreadCreateInputModelHook()
