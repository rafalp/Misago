from typing import Dict, List, Tuple, cast

from ariadne import MutationType
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ...errors import ErrorsList
from ...hooks import (
    edit_post_hook,
    edit_post_input_hook,
    edit_post_input_model_hook,
)
from ...loaders import load_post, load_thread, store_post
from ...threads.update import update_post
from ...types import (
    AsyncValidator,
    GraphQLContext,
    Post,
    EditPostInput,
    EditPostInputModel,
    Thread,
)
from ...validation import (
    CategoryIsOpenValidator,
    IsPostAuthorValidator,
    PostCategoryValidator,
    PostExistsValidator,
    PostThreadValidator,
    ThreadIsOpenValidator,
    validate_data,
    validate_model,
)
from ..decorators import error_handler, require_auth


edit_post_mutation = MutationType()


@edit_post_mutation.field("editPost")
@error_handler
@require_auth
async def resolve_edit_post(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await edit_post_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    post = await load_post(info.context, input["post"])
    if post:
        thread = await load_thread(info.context, post.thread_id)
    else:
        thread = None

    if cleaned_data:
        validators: Dict[str, List[AsyncValidator]] = {
            "post": [
                PostExistsValidator(info.context),
                IsPostAuthorValidator(info.context),
                PostCategoryValidator(
                    info.context, CategoryIsOpenValidator(info.context)
                ),
                PostThreadValidator(info.context, ThreadIsOpenValidator(info.context)),
            ],
        }
        cleaned_data, errors = await edit_post_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors, "thread": thread, "post": post}

    thread, post = await edit_post_hook.call_action(
        edit_post, info.context, cleaned_data
    )

    return {"thread": thread, "post": post}


async def create_input_model(context: GraphQLContext) -> EditPostInputModel:
    return create_model(
        "EditPostInputModel",
        post=(PositiveInt, ...),
        body=(constr(strip_whitespace=True), ...),
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
) -> Tuple[Thread, Post]:
    post = await update_post(
        cleaned_data["post"], body={"text": cleaned_data["body"]}, increment_edits=True
    )

    store_post(context, post)

    thread = await load_thread(context, post.thread_id)
    thread = cast(Thread, thread)

    return thread, post
