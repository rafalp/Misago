from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....errors import ErrorsList
from ....loaders import load_threads, store_threads
from ....threads.close import close_threads
from ....threads.models import Thread
from ....utils.lists import remove_none_items, update_list_items
from ....validation import (
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
    Validator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadsbulkclose import (
    ThreadsBulkCloseInput,
    threads_bulk_close_hook,
    threads_bulk_close_input_hook,
)

threads_bulk_close_mutation = MutationType()


@threads_bulk_close_mutation.field("threadsBulkClose")
@error_handler
@convert_kwargs_to_snake_case
async def resolve_threads_bulk_close(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
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
            ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }
        (cleaned_data, errors,) = await threads_bulk_close_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if is_valid(cleaned_data, errors):
        updated_threads = await threads_bulk_close_hook.call_action(
            threads_bulk_close_action, info.context, cleaned_data
        )

        result = {
            "threads": update_list_items(threads, updated_threads),
            "updated": sorted([thread.id for thread in updated_threads]),
        }
    else:
        result = {"threads": threads, "updated": []}

    if errors:
        result["errors"] = errors

    return result


def create_input_model(context: GraphQLContext) -> Type[BaseModel]:
    return create_model(
        "ThreadsBulkCloseInputModel",
        threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadsBulkCloseInput,
    errors: ErrorsList,
) -> Tuple[ThreadsBulkCloseInput, ErrorsList]:
    return await validate_data(data, validators, errors)


def is_valid(cleaned_data: ThreadsBulkCloseInput, errors: ErrorsList) -> bool:
    if errors.has_root_errors:
        return False

    return bool(cleaned_data.get("threads"))


async def threads_bulk_close_action(
    context: GraphQLContext, cleaned_data: ThreadsBulkCloseInput
) -> List[Thread]:
    threads = cleaned_data["threads"]
    threads = await close_threads(threads)
    store_threads(context, threads)

    return threads
