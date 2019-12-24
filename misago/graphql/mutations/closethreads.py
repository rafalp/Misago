from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ...errors import ErrorsList
from ...hooks import (
    close_threads_hook,
    close_threads_input_hook,
    close_threads_input_model_hook,
)
from ...loaders import load_threads, store_threads
from ...threads.close import close_threads
from ...types import (
    AsyncValidator,
    GraphQLContext,
    CloseThreadsInput,
    CloseThreadsInputModel,
    Thread,
)
from ...utils.lists import clear_list
from ...validation import (
    IsCategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
    UserIsAuthorizedRootValidator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


close_threads_mutation = MutationType()


@close_threads_mutation.field("closeThreads")
@error_handler
@convert_kwargs_to_snake_case
async def resolve_close_threads(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await close_threads_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("threads"):
        threads = clear_list(await load_threads(info.context, cleaned_data["threads"]))
    else:
        threads = []

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "threads": [
                ThreadsBulkValidator(
                    [
                        ThreadExistsValidator(info.context),
                        ThreadCategoryValidator(
                            info.context, IsCategoryModeratorValidator(info.context)
                        ),
                    ]
                ),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await close_threads_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "threads": threads or None}

    threads = await close_threads_hook.call_action(
        close_threads_action, info.context, cleaned_data
    )

    return {"threads": threads}


async def create_input_model(context: GraphQLContext) -> CloseThreadsInputModel:
    return create_model(
        "CloseThreadsInputModel",
        threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
        is_closed=(bool, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: CloseThreadsInput,
    errors: ErrorsList,
) -> Tuple[CloseThreadsInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def close_threads_action(
    context: GraphQLContext, cleaned_data: CloseThreadsInput
) -> List[Thread]:
    threads = cleaned_data["threads"]
    threads = await close_threads(threads, cleaned_data["is_closed"])
    store_threads(context, threads)

    return threads
