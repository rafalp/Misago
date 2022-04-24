from typing import Dict, List, Tuple, Type, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryIsOpenValidator
from ....context import Context
from ....richtext.parser import ParsedMarkupMetadata, parse_markup
from ....threads.loaders import posts_loader, threads_loader
from ....threads.models import Post, Thread
from ....threads.validators import (
    PostAuthorValidator,
    PostCategoryValidator,
    PostExistsValidator,
    PostThreadValidator,
    ThreadIsOpenValidator,
)
from ....validation import ErrorsList, Validator, validate_data, validate_model
from ...errorhandler import error_handler
from .hooks.postupdate import PostUpdateInput, post_update_hook, post_update_input_hook

post_update_mutation = MutationType()


@post_update_mutation.field("postUpdate")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_post_update(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    post = None
    thread = None

    if cleaned_data.get("post"):
        post = await posts_loader.load(info.context, input["post"])
        if post:
            thread = await threads_loader.load(info.context, post.thread_id)

    if cleaned_data:
        validators: Dict[str, List[Validator]] = {
            "post": [
                PostExistsValidator(info.context),
                PostAuthorValidator(info.context),
                PostCategoryValidator(
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                PostThreadValidator(info.context, ThreadIsOpenValidator(info.context)),
            ],
            ErrorsList.ROOT_LOCATION: [
                IsAuthenticatedValidator(info.context),
            ],
        }
        cleaned_data, errors = await post_update_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {
            "errors": errors,
            "thread": thread,
            "post": post,
            "updated": False,
        }

    thread, updated_post, _ = await post_update_hook.call_action(
        post_update, info.context, cleaned_data
    )

    return {
        "thread": thread,
        "post": updated_post,
        "updated": updated_post != post,
    }


def create_input_model(context: Context) -> Type[BaseModel]:
    return create_model(
        "PostUpdateInputModel",
        post=(PositiveInt, ...),
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
    data: PostUpdateInput,
    errors: ErrorsList,
) -> Tuple[PostUpdateInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def post_update(
    context: Context, cleaned_data: PostUpdateInput
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

    post = cleaned_data["post"]
    post = await post.update(
        markup=cleaned_data["markup"],
        rich_text=rich_text,
        increment_edits=True,
    )

    posts_loader.store(context, post)

    thread = await threads_loader.load(context, post.thread_id)
    thread = cast(Thread, thread)

    return thread, post, metadata