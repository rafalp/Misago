from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import (
    CategoryExistsValidator,
    CategoryIsOpenValidator,
    CategoryModeratorValidator,
)
from ....loaders import load_threads, store_threads
from ....threads.models import Thread
from ....threads.move import move_threads
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
from .hooks.threadsbulkmove import (
    ThreadsBulkMoveInput,
    threads_bulk_move_hook,
    threads_bulk_move_input_hook,
)

threads_bulk_move_mutation = MutationType()


@threads_bulk_move_mutation.field("threadsBulkMove")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_threads_bulk_move(
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
                )
            ],
            "category": [
                CategoryExistsValidator(info.context),
                CategoryIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }
        cleaned_data, errors = await threads_bulk_move_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if is_valid(cleaned_data, errors):
        updated_threads = await threads_bulk_move_hook.call_action(
            threads_bulk_move_action, info.context, cleaned_data
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
        "ThreadsBulkMoveInputModel",
        threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
        category=(PositiveInt, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadsBulkMoveInput,
    errors: ErrorsList,
) -> Tuple[ThreadsBulkMoveInput, ErrorsList]:
    return await validate_data(data, validators, errors)


def is_valid(cleaned_data: ThreadsBulkMoveInput, errors_locations: ErrorsList) -> bool:
    if errors_locations.has_root_errors:
        return False
    if not cleaned_data.get("category") or not cleaned_data.get("threads"):
        return False
    return True


async def threads_bulk_move_action(
    context: GraphQLContext, cleaned_data: ThreadsBulkMoveInput
) -> List[Thread]:
    threads = cleaned_data["threads"]
    threads = await move_threads(threads, cleaned_data["category"])
    store_threads(context, threads)

    return threads
