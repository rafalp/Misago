from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....loaders import clear_all_posts, clear_thread
from ....threads.delete import delete_thread
from ....validation import (
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
from .hooks.deletethread import (
    DeleteThreadInput,
    DeleteThreadInputModel,
    delete_thread_hook,
    delete_thread_input_hook,
    delete_thread_input_model_hook,
)

delete_thread_mutation = MutationType()


@delete_thread_mutation.field("deleteThread")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_delete_thread(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await delete_thread_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

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
        cleaned_data, errors = await delete_thread_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "deleted": []}

    await delete_thread_hook.call_action(
        delete_thread_action, info.context, cleaned_data
    )

    return {"deleted": [cleaned_data["thread"].id]}


async def create_input_model(context: GraphQLContext) -> DeleteThreadInputModel:
    return create_model("DeleteThreadInputModel", thread=(PositiveInt, ...))


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: DeleteThreadInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def delete_thread_action(
    context: GraphQLContext, cleaned_data: DeleteThreadInput
):
    thread = cleaned_data["thread"]
    await delete_thread(thread)
    clear_thread(context, thread)
    clear_all_posts(context)
