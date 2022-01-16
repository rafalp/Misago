from asyncio import gather
from typing import Dict, List, Tuple, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ....categories.models import Category
from ....errors import ErrorsList
from ....loaders import (
    load_category,
    load_thread,
    store_category,
    store_post,
    store_thread,
)
from ....pubsub.threads import publish_thread_update
from ....richtext import ParsedMarkupMetadata, parse_markup
from ....threads.hooks import create_post_hook
from ....threads.models import Post, Thread
from ....validation import (
    CategoryIsOpenValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
    UserIsAuthorizedRootValidator,
    Validator,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.postcreate import (
    PostCreateInput,
    PostCreateInputModel,
    post_create_hook,
    post_create_input_hook,
    post_create_input_model_hook,
)

post_create_mutation = MutationType()


@post_create_mutation.field("postCreate")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_post_create(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await post_create_input_model_hook.call_action(
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
            ErrorsList.ROOT_LOCATION: [
                UserIsAuthorizedRootValidator(info.context),
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


async def create_input_model(context: GraphQLContext) -> PostCreateInputModel:
    return create_model(
        "PostCreateInputModel",
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
    data: PostCreateInput,
    errors: ErrorsList,
) -> Tuple[PostCreateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def post_create(
    context: GraphQLContext, cleaned_data: PostCreateInput
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    thread = cleaned_data["thread"]
    rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

    def create_post(*args, **kwargs):
        return Post.create(*args, **kwargs)

    reply = await create_post_hook.call_action(
        create_post,
        thread,
        cleaned_data["markup"],
        rich_text,
        poster=context["user"],
        context=context,
    )
    category = cast(Category, await load_category(context, thread.category_id))

    thread, category = await gather(
        thread.update(last_post=reply, increment_replies=True),
        category.update(increment_posts=True),
    )

    store_category(context, category)
    store_thread(context, thread)
    store_post(context, reply)

    await publish_thread_update(thread)

    return thread, reply, metadata
