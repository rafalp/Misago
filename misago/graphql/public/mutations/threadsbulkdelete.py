from typing import Any, Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryModeratorValidator
from ....errors import ErrorsList
from ....loaders import clear_all_posts, clear_threads, load_threads
from ....threads.models import Thread
from ....threads.validators import (
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
)
from ....validation import Validator, bulkactionidslist, validate_data, validate_model
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadsbulkdelete import (
    ThreadsBulkDeleteInput,
    threads_bulk_delete_hook,
    threads_bulk_delete_input_hook,
)

threads_bulk_delete_mutation = MutationType()


@threads_bulk_delete_mutation.field("threadsBulkDelete")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_threads_bulk_delete(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("threads"):
        # prime threads cache for bulk action
        await load_threads(info.context, cleaned_data["threads"])

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
            ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }
        cleaned_data, errors = await threads_bulk_delete_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    result: Dict[str, Any] = {"deleted": []}

    if is_valid(cleaned_data, errors):
        await threads_bulk_delete_hook.call_action(
            threads_bulk_delete_action, info.context, cleaned_data
        )
        result["deleted"] = [i.id for i in cleaned_data["threads"]]

    if errors:
        result["errors"] = errors

    return result


def create_input_model(context: GraphQLContext) -> Type[BaseModel]:
    return create_model(
        "ThreadsBulkDeleteInputModel",
        threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadsBulkDeleteInput,
    errors: ErrorsList,
) -> Tuple[ThreadsBulkDeleteInput, ErrorsList]:
    return await validate_data(data, validators, errors)


def is_valid(
    cleaned_data: ThreadsBulkDeleteInput, errors_locations: ErrorsList
) -> bool:
    if errors_locations.has_root_errors:
        return False
    if not cleaned_data.get("threads"):
        return False
    return True


async def threads_bulk_delete_action(
    context: GraphQLContext, cleaned_data: ThreadsBulkDeleteInput
):
    threads_ids = [thread.id for thread in cleaned_data["threads"]]
    await Thread.query.filter(id__in=threads_ids).delete()
    clear_threads(context, cleaned_data["threads"])
    clear_all_posts(context)
