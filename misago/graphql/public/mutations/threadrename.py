from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....errors import ErrorsList
from ....loaders import load_thread, store_thread
from ....threads.models import Thread
from ....validation import (
    CategoryIsOpenValidator,
    ThreadAuthorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
    Validator,
    threadtitlestr,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadrename import (
    ThreadRenameInput,
    thread_rename_hook,
    thread_rename_input_hook,
)

thread_rename_mutation = MutationType()


@thread_rename_mutation.field("threadRename")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_thread_rename(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadAuthorValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                ThreadIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [
                IsAuthenticatedValidator(info.context),
            ],
        }
        cleaned_data, errors = await thread_rename_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread, "updated": False}

    updated_thread = await thread_rename_hook.call_action(
        thread_rename, info.context, cleaned_data
    )

    return {"thread": updated_thread, "updated": updated_thread != thread}


def create_input_model(context: GraphQLContext) -> Type[BaseModel]:
    return create_model(
        "ThreadRenameInputModel",
        thread=(PositiveInt, ...),
        title=(threadtitlestr(context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadRenameInput,
    errors: ErrorsList,
) -> Tuple[ThreadRenameInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_rename(
    context: GraphQLContext, cleaned_data: ThreadRenameInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await thread.update(title=cleaned_data["title"])

    store_thread(context, thread)

    return thread
