from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....hooks import (
    edit_thread_title_hook,
    edit_thread_title_input_hook,
    edit_thread_title_input_model_hook,
)
from ....loaders import load_thread, store_thread
from ....threads.update import update_thread
from ....types import (
    EditThreadTitleInput,
    EditThreadTitleInputModel,
    GraphQLContext,
    Thread,
    Validator,
)
from ....validation import (
    CategoryIsOpenValidator,
    ThreadAuthorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
    UserIsAuthorizedRootValidator,
    threadtitlestr,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler

edit_thread_title_mutation = MutationType()


@edit_thread_title_mutation.field("editThreadTitle")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_edit_thread_title(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await edit_thread_title_input_model_hook.call_action(
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
        cleaned_data, errors = await edit_thread_title_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await edit_thread_title_hook.call_action(
        edit_thread_title, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> EditThreadTitleInputModel:
    return create_model(
        "EditThreadTitleInputModel",
        thread=(PositiveInt, ...),
        title=(threadtitlestr(context["settings"]), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: EditThreadTitleInput,
    errors: ErrorsList,
) -> Tuple[EditThreadTitleInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def edit_thread_title(
    context: GraphQLContext, cleaned_data: EditThreadTitleInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread = await update_thread(thread, title=cleaned_data["title"])

    store_thread(context, thread)

    return thread
