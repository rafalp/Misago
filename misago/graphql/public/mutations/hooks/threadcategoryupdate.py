from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....threads.models import Thread
from .....validation import Validator
from .... import GraphQLContext

ThreadCategoryUpdateInputModel = Type[BaseModel]
ThreadCategoryUpdateInputModelAction = Callable[
    [GraphQLContext], Awaitable[ThreadCategoryUpdateInputModel]
]
ThreadCategoryUpdateInputModelFilter = Callable[
    [ThreadCategoryUpdateInputModelAction, GraphQLContext],
    Awaitable[ThreadCategoryUpdateInputModel],
]


class ThreadCategoryUpdateInputModelHook(
    FilterHook[
        ThreadCategoryUpdateInputModelAction, ThreadCategoryUpdateInputModelFilter
    ]
):
    def call_action(
        self, action: ThreadCategoryUpdateInputModelAction, context: GraphQLContext
    ) -> Awaitable[ThreadCategoryUpdateInputModel]:
        return self.filter(action, context)


ThreadCategoryUpdateInput = Dict[str, Any]
ThreadCategoryUpdateInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], ThreadCategoryUpdateInput, ErrorsList],
    Awaitable[Tuple[ThreadCategoryUpdateInput, ErrorsList]],
]
ThreadCategoryUpdateInputFilter = Callable[
    [ThreadCategoryUpdateInputAction, GraphQLContext, ThreadCategoryUpdateInput],
    Awaitable[Tuple[ThreadCategoryUpdateInput, ErrorsList]],
]


class ThreadCategoryUpdateInputHook(
    FilterHook[ThreadCategoryUpdateInputAction, ThreadCategoryUpdateInputFilter]
):
    def call_action(
        self,
        action: ThreadCategoryUpdateInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadCategoryUpdateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadCategoryUpdateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadCategoryUpdateAction = Callable[
    [GraphQLContext, ThreadCategoryUpdateInput], Awaitable[Thread]
]
ThreadCategoryUpdateFilter = Callable[
    [ThreadCategoryUpdateAction, GraphQLContext, ThreadCategoryUpdateInput],
    Awaitable[Thread],
]


class ThreadCategoryUpdateHook(
    FilterHook[ThreadCategoryUpdateAction, ThreadCategoryUpdateFilter]
):
    def call_action(
        self,
        action: ThreadCategoryUpdateAction,
        context: GraphQLContext,
        cleaned_data: ThreadCategoryUpdateInput,
    ) -> Awaitable[Thread]:
        return self.filter(action, context, cleaned_data)


thread_category_update_hook = ThreadCategoryUpdateHook()
thread_category_update_input_hook = ThreadCategoryUpdateInputHook()
thread_category_update_input_model_hook = ThreadCategoryUpdateInputModelHook()
