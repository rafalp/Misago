from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....loaders import load_thread, store_thread
from ....threads.models import Thread
from ....threads.move import move_thread
from ....validation import (
    CategoryExistsValidator,
    CategoryIsOpenValidator,
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    UserIsAuthorizedRootValidator,
    Validator,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadcategoryupdate import (
    ThreadCategoryUpdateInput,
    ThreadCategoryUpdateInputModel,
    thread_category_update_hook,
    thread_category_update_input_hook,
    thread_category_update_input_model_hook,
)

thread_category_update_mutation = MutationType()


@thread_category_update_mutation.field("threadCategoryUpdate")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_move_thread(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await thread_category_update_input_model_hook.call_action(
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
        cleaned_data, errors = await thread_category_update_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await thread_category_update_hook.call_action(
        thread_category_update_action, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> ThreadCategoryUpdateInputModel:
    return create_model(
        "ThreadCategoryUpdateInputModel",
        thread=(PositiveInt, ...),
        category=(PositiveInt, ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadCategoryUpdateInput,
    errors: ErrorsList,
) -> Tuple[ThreadCategoryUpdateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_category_update_action(
    context: GraphQLContext, cleaned_data: ThreadCategoryUpdateInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await move_thread(thread, cleaned_data["category"])

    store_thread(context, thread)

    return thread
