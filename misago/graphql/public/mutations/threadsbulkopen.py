from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryModeratorValidator
from ....threads.close import open_threads
from ....threads.loaders import threads_loader
from ....threads.models import Thread
from ....threads.validators import (
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
)
from ....utils.lists import remove_none_items, update_list_items
from ....validation import (
    ErrorsList,
    Validator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadsbulkopen import (
    ThreadsBulkOpenInput,
    threads_bulk_open_hook,
    threads_bulk_open_input_hook,
)

threads_bulk_open_mutation = MutationType()


@threads_bulk_open_mutation.field("threadsBulkOpen")
@error_handler
@convert_kwargs_to_snake_case
async def resolve_threads_bulk_open(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("threads"):
        threads = remove_none_items(
            await threads_loader.load_many(info.context, cleaned_data["threads"])
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
        (cleaned_data, errors,) = await threads_bulk_open_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if is_valid(cleaned_data, errors):
        updated_threads = await threads_bulk_open_hook.call_action(
            threads_bulk_open_action, info.context, cleaned_data
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
        "ThreadsBulkOpenInputModel",
        threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadsBulkOpenInput,
    errors: ErrorsList,
) -> Tuple[ThreadsBulkOpenInput, ErrorsList]:
    return await validate_data(data, validators, errors)


def is_valid(cleaned_data: ThreadsBulkOpenInput, errors: ErrorsList) -> bool:
    if errors.has_root_errors:
        return False

    return bool(cleaned_data.get("threads"))


async def threads_bulk_open_action(
    context: GraphQLContext, cleaned_data: ThreadsBulkOpenInput
) -> List[Thread]:
    threads = cleaned_data["threads"]
    threads = await open_threads(threads)
    threads_loader.store_many(context, threads)

    return threads
