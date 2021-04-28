from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....loaders import load_thread, store_thread
from ....threads.close import close_thread
from ....threads.models import Thread
from ....types import Validator
from ....validation import (
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    UserIsAuthorizedRootValidator,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.closethread import (
    CloseThreadInput,
    CloseThreadInputModel,
    close_thread_hook,
    close_thread_input_hook,
    close_thread_input_model_hook,
)

close_thread_mutation = MutationType()


@close_thread_mutation.field("closeThread")
@error_handler
@convert_kwargs_to_snake_case
async def resolve_close_thread(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await close_thread_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await close_thread_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await close_thread_hook.call_action(
        close_thread_action, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> CloseThreadInputModel:
    return create_model(
        "CloseThreadInputModel",
        thread=(PositiveInt, ...),
        is_closed=(bool, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: CloseThreadInput,
    errors: ErrorsList,
) -> Tuple[CloseThreadInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def close_thread_action(
    context: GraphQLContext, cleaned_data: CloseThreadInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await close_thread(thread, cleaned_data["is_closed"])

    store_thread(context, thread)

    return thread
