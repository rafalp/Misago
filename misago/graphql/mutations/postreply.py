from typing import Dict, List, Tuple

from ariadne import MutationType
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ...auth import get_authenticated_user
from ...errors import ErrorsList, NotAuthorizedError
from ...hooks import (
    create_post_hook,
    post_thread_hook,
    post_thread_input_hook,
    post_thread_input_model_hook,
)
from ...loaders import load_thread, store_post, store_thread
from ...threads.create import create_post
from ...threads.update import update_thread
from ...types import (
    AsyncValidator,
    GraphQLContext,
    Post,
    PostThreadInput,
    PostThreadInputModel,
    Thread,
)
from ...validation import (
    CategoryIsOpenValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


post_reply_mutation = MutationType()


@post_reply_mutation.field("postReply")
@error_handler
async def resolve_post_reply(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    user = await get_authenticated_user(info.context)
    if not user:
        raise NotAuthorizedError()

    input_model = await post_thread_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    thread = await load_thread(info.context, input["thread"])

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                ThreadIsOpenValidator(info.context),
            ],
        }
        cleaned_data, errors = await post_thread_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread, post = await post_thread_hook.call_action(
        post_reply, info.context, cleaned_data
    )

    return {"thread": thread, "post": post}


async def create_input_model(context: GraphQLContext) -> PostThreadInputModel:
    return create_model(
        "PostThreadInputModel",
        thread=(PositiveInt, ...),
        body=(constr(strip_whitespace=True), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: PostThreadInput,
    errors: ErrorsList,
) -> Tuple[PostThreadInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def post_reply(
    context: GraphQLContext, cleaned_data: PostThreadInput
) -> Tuple[Thread, Post]:
    thread = cleaned_data["thread"]
    user = await get_authenticated_user(context)
    reply = await create_post_hook.call_action(
        create_post, thread, {"text": cleaned_data["body"]}, poster=user
    )
    thread = await update_thread(thread, last_post=reply, increment_replies=True)

    store_thread(context, thread)
    store_post(context, reply)

    return thread, reply
