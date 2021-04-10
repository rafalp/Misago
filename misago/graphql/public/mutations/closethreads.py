from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....hooks.closethreads import (
    CloseThreadsInput,
    CloseThreadsInputModel,
    close_threads_hook,
    close_threads_input_hook,
    close_threads_input_model_hook,
)
from ....loaders import load_threads, store_threads
from ....threads.close import close_threads
from ....types import GraphQLContext, Thread, Validator
from ....utils.lists import remove_none_items, update_list_items
from ....validation import (
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
    UserIsAuthorizedRootValidator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler

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
        threads = remove_none_items(
            await load_threads(info.context, cleaned_data["threads"])
        )
    else:
        threads = []

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "threads": [
                ThreadsBulkValidator(
                    [
                        ThreadExistsValidator(info.context),
                        ThreadCategoryValidator(
                            info.context, CategoryModeratorValidator(info.context)
                        ),
                    ]
                ),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await close_threads_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if is_valid(cleaned_data, errors):
        updated_threads = await close_threads_hook.call_action(
            close_threads_action, info.context, cleaned_data
        )

        result = {
            "threads": update_list_items(threads, updated_threads),
            "updated": True,
        }
    else:
        result = {"threads": threads, "updated": False}

    if errors:
        result["errors"] = errors

    return result


async def create_input_model(context: GraphQLContext) -> CloseThreadsInputModel:
    return create_model(
        "CloseThreadsInputModel",
        threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
        is_closed=(bool, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: CloseThreadsInput,
    errors: ErrorsList,
) -> Tuple[CloseThreadsInput, ErrorsList]:
    return await validate_data(data, validators, errors)


def is_valid(cleaned_data: CloseThreadsInput, errors: ErrorsList) -> bool:
    if errors.has_root_errors:
        return False
    if not cleaned_data.get("threads") or "is_closed" not in cleaned_data:
        return False
    return True


async def close_threads_action(
    context: GraphQLContext, cleaned_data: CloseThreadsInput
) -> List[Thread]:
    threads = cleaned_data["threads"]
    threads = await close_threads(threads, cleaned_data["is_closed"])
    store_threads(context, threads)

    return threads
