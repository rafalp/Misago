from typing import Any, Awaitable, Callable, Dict, List, Tuple

from .....context import Context
from .....hooks import FilterHook
from .....validation import ErrorsList, Validator

ThreadDeleteInput = Dict[str, Any]
ThreadDeleteInputAction = Callable[
    [Context, Dict[str, List[Validator]], ThreadDeleteInput, ErrorsList],
    Awaitable[Tuple[ThreadDeleteInput, ErrorsList]],
]
ThreadDeleteInputFilter = Callable[
    [ThreadDeleteInputAction, Context, ThreadDeleteInput],
    Awaitable[Tuple[ThreadDeleteInput, ErrorsList]],
]


class ThreadDeleteInputHook(
    FilterHook[ThreadDeleteInputAction, ThreadDeleteInputFilter]
):
    def call_action(
        self,
        action: ThreadDeleteInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadDeleteInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadDeleteInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadDeleteAction = Callable[[Context, ThreadDeleteInput], Awaitable[None]]
ThreadDeleteFilter = Callable[
    [ThreadDeleteAction, Context, ThreadDeleteInput], Awaitable[None]
]


class ThreadDeleteHook(FilterHook[ThreadDeleteAction, ThreadDeleteFilter]):
    async def call_action(
        self,
        action: ThreadDeleteAction,
        context: Context,
        cleaned_data: ThreadDeleteInput,
    ):
        await self.filter(action, context, cleaned_data)


thread_delete_hook = ThreadDeleteHook()
thread_delete_input_hook = ThreadDeleteInputHook()
