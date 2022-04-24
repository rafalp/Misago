from asyncio import gather
from typing import Dict, List, Tuple, Type, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.loaders import categories_loader
from ....categories.models import Category
from ....categories.validators import CategoryIsOpenValidator
from ....context import Context
from ....pubsub.threads import publish_thread_update
from ....richtext import ParsedMarkupMetadata, parse_markup
from ....threads.loaders import posts_loader, threads_loader
from ....threads.models import Post, Thread
from ....threads.validators import (
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
)
from ....validation import ErrorsList, Validator, validate_data, validate_model
from ...errorhandler import error_handler
from .hooks.postcreate import PostCreateInput, post_create_hook, post_create_input_hook

post_create_mutation = MutationType()


@post_create_mutation.field("postCreate")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_post_create(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
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
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                ThreadIsOpenValidator(info.context),
            ],
            ErrorsList.ROOT_LOCATION: [
                IsAuthenticatedValidator(info.context),
            ],
        }
        cleaned_data, errors = await post_create_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread}

    thread, post, _ = await post_create_hook.call_action(
        post_create, info.context, cleaned_data
    )

    return {"thread": thread, "post": post}


def create_input_model(context: Context) -> Type[BaseModel]:
    return create_model(
        "PostCreateInputModel",
        thread=(PositiveInt, ...),
        markup=(
            constr(
                strip_whitespace=True,
                min_length=context["settings"]["post_min_length"],
            ),
            ...,
        ),
    )


async def validate_input_data(
    context: Context,
    validators: Dict[str, List[Validator]],
    data: PostCreateInput,
    errors: ErrorsList,
) -> Tuple[PostCreateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def post_create(
    context: Context, cleaned_data: PostCreateInput
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    thread = cleaned_data["thread"]
    rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

    reply = await Post.create(
        thread,
        cleaned_data["markup"],
        rich_text,
        poster=context["user"],
    )
    category = cast(Category, await categories_loader.load(context, thread.category_id))

    thread, category = await gather(
        thread.update(last_post=reply, increment_replies=True),
        category.update(increment_posts=True),
    )

    categories_loader.store(context, category)
    threads_loader.store(context, thread)
    posts_loader.store(context, reply)

    await publish_thread_update(thread)

    return thread, reply, metadata