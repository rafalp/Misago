from asyncio import gather
from typing import Dict, List, Optional, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryExistsValidator
from ....database import database
from ....errors import ErrorsList
from ....loaders import store_category, store_post, store_thread
from ....pubsub.threads import publish_thread_update
from ....richtext import ParsedMarkupMetadata, parse_markup
from ....threads.models import Post, Thread
from ....validation import (
    CategoryIsOpenValidator,
    NewThreadIsClosedValidator,
    Validator,
    threadtitlestr,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.threadcreate import (
    ThreadCreateInput,
    thread_create_hook,
    thread_create_input_hook,
)

thread_create_mutation = MutationType()


@thread_create_mutation.field("threadCreate")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_thread_create(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "category": [
                CategoryExistsValidator(info.context),
                CategoryIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [
                IsAuthenticatedValidator(info.context),
            ],
        }

        if cleaned_data.get("is_closed") and cleaned_data.get("category"):
            validators["is_closed"] = [
                NewThreadIsClosedValidator(info.context, cleaned_data["category"])
            ]

        cleaned_data, errors = await thread_create_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors}

    thread, _, _ = await thread_create_hook.call_action(
        thread_create, info.context, cleaned_data
    )

    return {"thread": thread}


def create_input_model(context: GraphQLContext) -> Type[BaseModel]:
    return create_model(
        "ThreadCreateInputModel",
        category=(PositiveInt, ...),
        title=(threadtitlestr(context["settings"]), ...),
        markup=(
            constr(
                strip_whitespace=True,
                min_length=context["settings"]["post_min_length"],
            ),
            ...,
        ),
        is_closed=(Optional[bool], False),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadCreateInput,
    errors: ErrorsList,
) -> Tuple[ThreadCreateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def thread_create(
    context: GraphQLContext, cleaned_data: ThreadCreateInput
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    user = context["user"]
    rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

    async with database.transaction():
        thread = await Thread.create(
            cleaned_data["category"],
            cleaned_data["title"],
            starter=user,
            is_closed=cleaned_data.get("is_closed") or False,
        )
        post = await Post.create(
            thread,
            cleaned_data["markup"],
            rich_text,
            poster=user,
        )
        category = cleaned_data["category"]
        thread, category = await gather(
            thread.update(first_post=post, last_post=post),
            category.update(increment_threads=True, increment_posts=True),
        )

    store_thread(context, thread)
    store_category(context, category)
    store_post(context, post)

    await publish_thread_update(thread)

    return thread, post, metadata
