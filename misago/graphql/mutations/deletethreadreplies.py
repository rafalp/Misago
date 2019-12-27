from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ...errors import ErrorsList
from ...hooks import (
    delete_thread_replies_hook,
    delete_thread_replies_input_model_hook,
    delete_thread_replies_input_replies_hook,
    delete_thread_replies_input_thread_hook,
)
from ...loaders import clear_posts, load_posts, load_thread, store_post, store_thread
from ...threads.delete import delete_thread_posts
from ...types import (
    AsyncValidator,
    GraphQLContext,
    DeleteThreadRepliesInput,
    DeleteThreadRepliesInputModel,
    Thread,
)
from ...validation import (
    CategoryModeratorValidator,
    PostsBulkValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadReplyExistsValidator,
    UserIsAuthorizedRootValidator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


delete_thread_replies_mutation = MutationType()


@delete_thread_replies_mutation.field("deleteThreadReplies")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_delete_thread_replies(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await delete_thread_replies_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if thread and cleaned_data.get("replies"):
        # prime posts cache for bulk action
        await load_posts(info.context, cleaned_data["replies"])

    if cleaned_data:
        thread_validators: Dict[str, List[AsyncValidator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        (
            cleaned_data,
            errors,
        ) = await delete_thread_replies_input_thread_hook.call_action(
            validate_input_thread_data,
            info.context,
            thread_validators,
            cleaned_data,
            errors,
        )

    if errors:
        return {"errors": errors, "thread": thread}

    if cleaned_data.get("thread"):
        replies_validators: Dict[str, List[AsyncValidator]] = {
            "replies": [
                PostsBulkValidator(
                    [ThreadReplyExistsValidator(info.context, cleaned_data["thread"]),]
                )
            ],
        }
        (
            cleaned_data,
            errors,
        ) = await delete_thread_replies_input_replies_hook.call_action(
            validate_input_replies_data,
            info.context,
            replies_validators,
            cleaned_data,
            errors,
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread = await delete_thread_replies_hook.call_action(
        delete_thread_replies_action, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> DeleteThreadRepliesInputModel:
    return create_model(
        "DeleteThreadRepliesInputModel",
        thread=(PositiveInt, ...),
        replies=(bulkactionidslist(PositiveInt, context["settings"]), ...),
    )


async def validate_input_replies_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: DeleteThreadRepliesInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadRepliesInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def validate_input_thread_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: DeleteThreadRepliesInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadRepliesInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def delete_thread_replies_action(
    context: GraphQLContext, cleaned_data: DeleteThreadRepliesInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread, last_post = await delete_thread_posts(thread, cleaned_data["replies"])
    clear_posts(context, cleaned_data["replies"])
    store_post(context, last_post)
    store_thread(context, thread)
    return thread
