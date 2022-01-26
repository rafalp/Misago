from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryModeratorValidator
from ....errors import ErrorsList
from ....loaders import clear_all_posts, clear_thread
from ....threads.validators import ThreadCategoryValidator, ThreadExistsValidator
from ....validation import Validator, validate_data, validate_model
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threaddelete import (
    ThreadDeleteInput,
    thread_delete_hook,
    thread_delete_input_hook,
)

thread_delete_mutation = MutationType()


@thread_delete_mutation.field("threadDelete")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_thread_delete(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model()
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }
        cleaned_data, errors = await thread_delete_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "deleted": False}

    await thread_delete_hook.call_action(
        thread_delete_action, info.context, cleaned_data
    )

    return {"deleted": True}


def create_input_model() -> Type[BaseModel]:
    return create_model("ThreadDeleteInputModel", thread=(PositiveInt, ...))


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadDeleteInput,
    errors: ErrorsList,
) -> Tuple[ThreadDeleteInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_delete_action(
    context: GraphQLContext, cleaned_data: ThreadDeleteInput
):
    thread = cleaned_data["thread"]
    await thread.delete()
    clear_thread(context, thread)
    clear_all_posts(context)
