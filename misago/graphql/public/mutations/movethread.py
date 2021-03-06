from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....hooks import (
    move_thread_hook,
    move_thread_input_hook,
    move_thread_input_model_hook,
)
from ....loaders import load_thread, store_thread
from ....threads.move import move_thread
from ....types import (
    GraphQLContext,
    MoveThreadInput,
    MoveThreadInputModel,
    Thread,
    Validator,
)
from ....validation import (
    CategoryExistsValidator,
    CategoryIsOpenValidator,
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    UserIsAuthorizedRootValidator,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler

move_thread_mutation = MutationType()


@move_thread_mutation.field("moveThread")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_move_thread(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await move_thread_input_model_hook.call_action(
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
            "category": [
                CategoryExistsValidator(info.context),
                CategoryIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await move_thread_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await move_thread_hook.call_action(
        move_thread_action, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> MoveThreadInputModel:
    return create_model(
        "MoveThreadInputModel", thread=(PositiveInt, ...), category=(PositiveInt, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: MoveThreadInput,
    errors: ErrorsList,
) -> Tuple[MoveThreadInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def move_thread_action(
    context: GraphQLContext, cleaned_data: MoveThreadInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await move_thread(thread, cleaned_data["category"])

    store_thread(context, thread)

    return thread
