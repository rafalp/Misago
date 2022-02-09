from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryModeratorValidator
from ....threads.loaders import threads_loader
from ....threads.models import Thread
from ....threads.validators import ThreadCategoryValidator, ThreadExistsValidator
from ....validation import ErrorsList, Validator, validate_data, validate_model
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadopen import ThreadOpenInput, thread_open_hook, thread_open_input_hook

thread_open_mutation = MutationType()


@thread_open_mutation.field("threadOpen")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_thread_open(
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
        cleaned_data, errors = await thread_open_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread, "updated": False}

    updated_thread = await thread_open_hook.call_action(
        thread_open_action, info.context, cleaned_data
    )

    return {"thread": updated_thread, "updated": updated_thread != thread}


def create_input_model() -> Type[BaseModel]:
    return create_model("ThreadOpenInputModel", thread=(PositiveInt, ...))


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadOpenInput,
    errors: ErrorsList,
) -> Tuple[ThreadOpenInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_open_action(
    context: GraphQLContext, cleaned_data: ThreadOpenInput
) -> Thread:
    thread = cleaned_data["thread"]
    if thread.is_closed:
        thread = await thread.update(is_closed=False)
        threads_loader.store(context, thread)

    return thread
