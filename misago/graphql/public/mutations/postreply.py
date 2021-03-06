from asyncio import gather
from typing import Dict, List, Tuple, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ....auth import get_authenticated_user
from ....categories.update import update_category
from ....errors import ErrorsList
from ....hooks import (
    create_post_hook,
    post_reply_hook,
    post_reply_input_hook,
    post_reply_input_model_hook,
)
from ....loaders import (
    load_category,
    load_thread,
    store_category,
    store_post,
    store_thread,
)
from ....pubsub.threads import publish_thread_update
from ....richtext import parse_markup
from ....threads.create import create_post
from ....threads.update import update_thread
from ....types import (
    Category,
    GraphQLContext,
    ParsedMarkupMetadata,
    Post,
    PostReplyInput,
    PostReplyInputModel,
    Thread,
    Validator,
)
from ....validation import (
    CategoryIsOpenValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
    UserIsAuthorizedRootValidator,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler

post_reply_mutation = MutationType()


@post_reply_mutation.field("postReply")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_post_reply(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await post_reply_input_model_hook.call_action(
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
                ThreadCategoryValidator(
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                ThreadIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context),],
        }
        cleaned_data, errors = await post_reply_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread, post, _ = await post_reply_hook.call_action(
        post_reply, info.context, cleaned_data
    )

    return {"thread": thread, "post": post}


async def create_input_model(context: GraphQLContext) -> PostReplyInputModel:
    return create_model(
        "PostReplyInputModel",
        thread=(PositiveInt, ...),
        markup=(
            constr(
                strip_whitespace=True, min_length=context["settings"]["post_min_length"]
            ),
            ...,
        ),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: PostReplyInput,
    errors: ErrorsList,
) -> Tuple[PostReplyInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def post_reply(
    context: GraphQLContext, cleaned_data: PostReplyInput
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    thread = cleaned_data["thread"]
    user = await get_authenticated_user(context)
    rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

    reply = await create_post_hook.call_action(
        create_post,
        thread,
        cleaned_data["markup"],
        rich_text,
        poster=user,
        context=context,
    )
    category = cast(Category, await load_category(context, thread.category_id))

    thread, category = await gather(
        update_thread(thread, last_post=reply, increment_replies=True),
        update_category(category, increment_posts=True),
    )

    store_category(context, category)
    store_thread(context, thread)
    store_post(context, reply)

    await publish_thread_update(thread)

    return thread, reply, metadata
