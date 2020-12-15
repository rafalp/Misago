from typing import Dict, List, Tuple, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ...errors import ErrorsList
from ...hooks import (
    edit_post_hook,
    edit_post_input_hook,
    edit_post_input_model_hook,
    update_post_hook,
)
from ...loaders import load_post, load_thread, store_post
from ...richtext.parser import parse_markup
from ...threads.update import update_post
from ...types import (
    AsyncValidator,
    GraphQLContext,
    EditPostInput,
    EditPostInputModel,
    ParsedMarkupMetadata,
    Post,
    Thread,
)
from ...validation import (
    CategoryIsOpenValidator,
    PostAuthorValidator,
    PostCategoryValidator,
    PostExistsValidator,
    PostThreadValidator,
    ThreadIsOpenValidator,
    UserIsAuthorizedRootValidator,
    validate_data,
    validate_model,
)
from ..errorhandler import error_handler


edit_post_mutation = MutationType()


@edit_post_mutation.field("editPost")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_edit_post(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await edit_post_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    post = None
    thread = None

    if cleaned_data.get("post"):
        post = await load_post(info.context, input["post"])
        if post:
            thread = await load_thread(info.context, post.thread_id)

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "post": [
                PostExistsValidator(info.context),
                PostAuthorValidator(info.context),
                PostCategoryValidator(
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                PostThreadValidator(info.context, ThreadIsOpenValidator(info.context)),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context),],
        }
        cleaned_data, errors = await edit_post_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread, "post": post}

    thread, post, _ = await edit_post_hook.call_action(
        edit_post, info.context, cleaned_data
    )

    return {"thread": thread, "post": post}


async def create_input_model(context: GraphQLContext) -> EditPostInputModel:
    return create_model(
        "EditPostInputModel",
        post=(PositiveInt, ...),
        markup=(
            constr(
                strip_whitespace=True, min_length=context["settings"]["post_min_length"]
            ),
            ...,
        ),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: EditPostInput,
    errors: ErrorsList,
) -> Tuple[EditPostInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def edit_post(
    context: GraphQLContext, cleaned_data: EditPostInput
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

    post = await update_post_hook.call_action(
        update_post,
        cleaned_data["post"],
        markup=cleaned_data["markup"],
        rich_text=rich_text,
        html=cleaned_data["markup"],
        increment_edits=True,
    )

    store_post(context, post)

    thread = await load_thread(context, post.thread_id)
    thread = cast(Thread, thread)

    return thread, post, metadata
