from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from ..types import GraphQLContext, Thread, Validator
from .filter import FilterHook


EditThreadTitleInputModel = Type[BaseModel]
EditThreadTitleInputModelAction = Callable[
    [GraphQLContext], Awaitable[EditThreadTitleInputModel]
]
EditThreadTitleInputModelFilter = Callable[
    [EditThreadTitleInputModelAction, GraphQLContext],
    Awaitable[EditThreadTitleInputModel],
]


class EditThreadTitleInputModelHook(
    FilterHook[EditThreadTitleInputModelAction, EditThreadTitleInputModelFilter]
):
    def call_action(
        self, action: EditThreadTitleInputModelAction, context: GraphQLContext
    ) -> Awaitable[EditThreadTitleInputModel]:
        return self.filter(action, context)


EditThreadTitleInput = Dict[str, Any]
EditThreadTitleInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        EditThreadTitleInput,
        ErrorsList,
    ],
    Awaitable[Tuple[EditThreadTitleInput, ErrorsList]],
]
EditThreadTitleInputFilter = Callable[
    [EditThreadTitleInputAction, GraphQLContext, EditThreadTitleInput],
    Awaitable[Tuple[EditThreadTitleInput, ErrorsList]],
]


class EditThreadTitleInputHook(
    FilterHook[EditThreadTitleInputAction, EditThreadTitleInputFilter]
):
    def call_action(
        self,
        action: EditThreadTitleInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: EditThreadTitleInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[EditThreadTitleInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


EditThreadTitleAction = Callable[
    [GraphQLContext, EditThreadTitleInput], Awaitable[Thread]
]
EditThreadTitleFilter = Callable[
    [EditThreadTitleAction, GraphQLContext, EditThreadTitleInput], Awaitable[Thread]
]


class EditThreadTitleHook(FilterHook[EditThreadTitleAction, EditThreadTitleFilter]):
    def call_action(
        self,
        action: EditThreadTitleAction,
        context: GraphQLContext,
        cleaned_data: EditThreadTitleInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


edit_thread_title_hook = EditThreadTitleHook()
edit_thread_title_input_hook = EditThreadTitleInputHook()
edit_thread_title_input_model_hook = EditThreadTitleInputModelHook()
