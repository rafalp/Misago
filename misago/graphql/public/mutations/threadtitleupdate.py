from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....loaders import load_thread, store_thread
from ....threads.models import Thread
from ....validation import (
    CategoryIsOpenValidator,
    ThreadAuthorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
    UserIsAuthorizedRootValidator,
    Validator,
    threadtitlestr,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadtitleupdate import (
    ThreadTitleUpdateInput,
    ThreadTitleUpdateInputModel,
    thread_title_update_hook,
    thread_title_update_input_hook,
    thread_title_update_input_model_hook,
)

thread_title_update_mutation = MutationType()


@thread_title_update_mutation.field("threadTitleUpdate")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_thread_title_update(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await thread_title_update_input_model_hook.call_action(
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
                ThreadAuthorValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                ThreadIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [
                UserIsAuthorizedRootValidator(info.context),
            ],
        }
        cleaned_data, errors = await thread_title_update_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await thread_title_update_hook.call_action(
        thread_title_update, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> ThreadTitleUpdateInputModel:
    return create_model(
        "ThreadTitleUpdateInputModel",
        thread=(PositiveInt, ...),
        title=(threadtitlestr(context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadTitleUpdateInput,
    errors: ErrorsList,
) -> Tuple[ThreadTitleUpdateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_title_update(
    context: GraphQLContext, cleaned_data: ThreadTitleUpdateInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await thread.update(title=cleaned_data["title"])

    store_thread(context, thread)

    return thread
