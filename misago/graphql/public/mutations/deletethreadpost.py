from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....loaders import clear_post, load_thread, store_post, store_thread
from ....threads.delete import delete_thread_post
from ....threads.models import Thread
from ....validation import (
    CategoryModeratorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadPostExistsValidator,
    ThreadPostIsReplyValidator,
    UserIsAuthorizedRootValidator,
    Validator,
    validate_data,
    validate_model,
)
from ... import GraphQLContext
from ...errorhandler import error_handler
from .hooks.deletethreadpost import (
    DeleteThreadPostInput,
    DeleteThreadPostInputModel,
    delete_thread_post_hook,
    delete_thread_post_input_model_hook,
    delete_thread_post_input_post_hook,
    delete_thread_post_input_thread_hook,
)

delete_thread_post_mutation = MutationType()


@delete_thread_post_mutation.field("deleteThreadPost")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_delete_thread_post(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await delete_thread_post_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if cleaned_data:
        thread_validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ErrorsList.ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }
        cleaned_data, errors = await delete_thread_post_input_thread_hook.call_action(
            validate_input_thread_data,
            info.context,
            thread_validators,
            cleaned_data,
            errors,
        )

    if errors:
        return {"errors": errors, "thread": thread, "deleted": []}

    if cleaned_data.get("thread"):
        post_validators: Dict[str, List[Validator]] = {
            "post": [
                ThreadPostExistsValidator(info.context, cleaned_data["thread"]),
                ThreadPostIsReplyValidator(cleaned_data["thread"]),
            ],
        }
        cleaned_data, errors = await delete_thread_post_input_post_hook.call_action(
            validate_input_post_data,
            info.context,
            post_validators,
            cleaned_data,
            errors,
        )

    if errors:
        return {"errors": errors, "thread": thread, "deleted": []}

    thread = await delete_thread_post_hook.call_action(
        delete_thread_post_action, info.context, cleaned_data
    )

    return {"thread": thread, "deleted": [cleaned_data["post"].id]}


async def create_input_model(context: GraphQLContext) -> DeleteThreadPostInputModel:
    return create_model(
        "DeleteThreadPostInputModel",
        thread=(PositiveInt, ...),
        post=(PositiveInt, ...),
    )


async def validate_input_post_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: DeleteThreadPostInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadPostInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def validate_input_thread_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: DeleteThreadPostInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadPostInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def delete_thread_post_action(
    context: GraphQLContext, cleaned_data: DeleteThreadPostInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread, last_post = await delete_thread_post(thread, cleaned_data["post"])
    clear_post(context, cleaned_data["post"])
    store_post(context, last_post)
    store_thread(context, thread)
    return thread
