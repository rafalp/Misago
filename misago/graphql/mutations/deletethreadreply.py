from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ...errors import ErrorsList
from ...hooks import (
    delete_thread_reply_hook,
    delete_thread_reply_input_model_hook,
    delete_thread_reply_input_reply_hook,
    delete_thread_reply_input_thread_hook,
)
from ...loaders import clear_post, load_thread, store_post, store_thread
from ...threads.delete import delete_thread_post
from ...types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadReplyInput,
    DeleteThreadReplyInputModel,
    Thread,
)
from ...validation import (
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadReplyExistsValidator,
    UserIsAuthorizedRootValidator,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


delete_thread_reply_mutation = MutationType()


@delete_thread_reply_mutation.field("deleteThreadReply")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_delete_thread_reply(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await delete_thread_reply_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await delete_thread_reply_input_thread_hook.call_action(
            validate_input_thread_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "reply": [
                ThreadReplyExistsValidator(info.context, cleaned_data.get("thread")),
            ],
        }
        cleaned_data, errors = await delete_thread_reply_input_reply_hook.call_action(
            validate_input_reply_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await delete_thread_reply_hook.call_action(
        delete_thread_reply_action, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> DeleteThreadReplyInputModel:
    return create_model(
        "DeleteThreadReplyInputModel",
        thread=(PositiveInt, ...),
        reply=(PositiveInt, ...),
    )


async def validate_input_reply_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: DeleteThreadReplyInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadReplyInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def validate_input_thread_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: DeleteThreadReplyInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadReplyInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def delete_thread_reply_action(
    context: GraphQLContext, cleaned_data: DeleteThreadReplyInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread, last_post = await delete_thread_post(thread, cleaned_data["reply"])
    clear_post(context, cleaned_data["reply"])
    store_post(context, last_post)
    store_thread(context, thread)
    return thread
