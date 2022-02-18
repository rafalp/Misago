from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryModeratorValidator
from ....context import Context
from ....threads.loaders import threads_loader
from ....threads.models import Thread
from ....threads.validators import ThreadCategoryValidator, ThreadExistsValidator
from ....validation import ErrorsList, Validator, validate_data, validate_model
from ...errorhandler import error_handler
from .hooks.threadclose import (
    ThreadCloseInput,
    thread_close_hook,
    thread_close_input_hook,
)

thread_close_mutation = MutationType()


@thread_close_mutation.field("threadClose")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_thread_close(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model()
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await threads_loader.load(info.context, cleaned_data["thread"])
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
            ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }
        cleaned_data, errors = await thread_close_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread, "updated": False}

    updated_thread = await thread_close_hook.call_action(
        thread_close_action, info.context, cleaned_data
    )

    return {"thread": updated_thread, "updated": updated_thread != thread}


def create_input_model() -> Type[BaseModel]:
    return create_model("ThreadCloseInputModel", thread=(PositiveInt, ...))


async def validate_input_data(
    context: Context,
    validators: Dict[str, List[Validator]],
    data: ThreadCloseInput,
    errors: ErrorsList,
) -> Tuple[ThreadCloseInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_close_action(
    context: Context, cleaned_data: ThreadCloseInput
) -> Thread:
    thread = cleaned_data["thread"]
    if not thread.is_closed:
        thread = await thread.update(is_closed=True)
        threads_loader.store(context, thread)

    return thread
