from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....hooks import FilterHook
from .....validation import ErrorsList, Validator
from .... import GraphQLContext

ThreadsBulkDeleteInput = Dict[str, Any]
ThreadsBulkDeleteInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], ThreadsBulkDeleteInput, ErrorsList],
    Awaitable[Tuple[ThreadsBulkDeleteInput, ErrorsList]],
]
ThreadsBulkDeleteInputFilter = Callable[
    [ThreadsBulkDeleteInputAction, GraphQLContext, ThreadsBulkDeleteInput],
    Awaitable[Tuple[ThreadsBulkDeleteInput, ErrorsList]],
]


class ThreadsBulkDeleteInputHook(
    FilterHook[ThreadsBulkDeleteInputAction, ThreadsBulkDeleteInputFilter]
):
    def call_action(
        self,
        action: ThreadsBulkDeleteInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkDeleteInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadsBulkDeleteInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadsBulkDeleteAction = Callable[
    [GraphQLContext, ThreadsBulkDeleteInput], Awaitable[None]
]
ThreadsBulkDeleteFilter = Callable[
    [ThreadsBulkDeleteAction, GraphQLContext, ThreadsBulkDeleteInput], Awaitable[None]
]


class ThreadsBulkDeleteHook(
    FilterHook[ThreadsBulkDeleteAction, ThreadsBulkDeleteFilter]
):
    async def call_action(
        self,
        action: ThreadsBulkDeleteAction,
        context: GraphQLContext,
        cleaned_data: ThreadsBulkDeleteInput,
    ):
        await self.filter(action, context, cleaned_data)


threads_bulk_delete_hook = ThreadsBulkDeleteHook()
threads_bulk_delete_input_hook = ThreadsBulkDeleteInputHook()
