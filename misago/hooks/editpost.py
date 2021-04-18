from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from ..types import (
    GraphQLContext,
    ParsedMarkupMetadata,
    Post,
    Thread,
    Validator,
)
from .filter import FilterHook

EditPostInputModel = Type[BaseModel]
EditPostInputModelAction = Callable[[GraphQLContext], Awaitable[EditPostInputModel]]
EditPostInputModelFilter = Callable[
    [EditPostInputModelAction, GraphQLContext],
    Awaitable[EditPostInputModel],
]


class EditPostInputModelHook(
    FilterHook[EditPostInputModelAction, EditPostInputModelFilter]
):
    def call_action(
        self, action: EditPostInputModelAction, context: GraphQLContext
    ) -> Awaitable[EditPostInputModel]:
        return self.filter(action, context)


EditPostInput = Dict[str, Any]
EditPostInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        EditPostInput,
        ErrorsList,
    ],
    Awaitable[Tuple[EditPostInput, ErrorsList]],
]
EditPostInputFilter = Callable[
    [EditPostInputAction, GraphQLContext, EditPostInput],
    Awaitable[Tuple[EditPostInput, ErrorsList]],
]


class EditPostInputHook(FilterHook[EditPostInputAction, EditPostInputFilter]):
    def call_action(
        self,
        action: EditPostInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: EditPostInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[EditPostInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


EditPostAction = Callable[
    [GraphQLContext, EditPostInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
EditPostFilter = Callable[
    [EditPostAction, GraphQLContext, EditPostInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]


class EditPostHook(FilterHook[EditPostAction, EditPostFilter]):
    def call_action(
        self,
        action: EditPostAction,
        context: GraphQLContext,
        cleaned_data: EditPostInput,
    ) -> Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]]:
        return self.filter(action, context, cleaned_data)


edit_post_hook = EditPostHook()
edit_post_input_hook = EditPostInputHook()
edit_post_input_model_hook = EditPostInputModelHook()
