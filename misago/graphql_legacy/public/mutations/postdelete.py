from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryModeratorValidator
from ....context import Context
from ....threads.delete import delete_thread_post
from ....threads.loaders import posts_loader, threads_loader
from ....threads.models import Thread
from ....threads.validators import (
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadPostExistsValidator,
    ThreadPostIsReplyValidator,
)
from ....validation import ErrorsList, Validator, validate_data, validate_model
from ...errorhandler import error_handler
from .hooks.postdelete import (
    PostDeleteInput,
    post_delete_hook,
    post_delete_input_post_hook,
    post_delete_input_thread_hook,
)

post_delete_mutation = MutationType()


@post_delete_mutation.field("postDelete")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_post_delete(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model()
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await threads_loader.load(info.context, cleaned_data["thread"])
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
            ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }
        cleaned_data, errors = await post_delete_input_thread_hook.call_action(
            validate_input_thread_data,
            info.context,
            thread_validators,
            cleaned_data,
            errors,
        )

    if errors:
        return {"errors": errors, "thread": thread, "deleted": False}

    if cleaned_data.get("thread"):
        post_validators: Dict[str, List[Validator]] = {
            "post": [
                ThreadPostExistsValidator(info.context, cleaned_data["thread"]),
                ThreadPostIsReplyValidator(cleaned_data["thread"]),
            ],
        }
        cleaned_data, errors = await post_delete_input_post_hook.call_action(
            validate_input_post_data,
            info.context,
            post_validators,
            cleaned_data,
            errors,
        )

    if errors:
        return {"errors": errors, "thread": thread, "deleted": False}

    thread = await post_delete_hook.call_action(
        post_delete_action, info.context, cleaned_data
    )

    return {"thread": thread, "deleted": True}


def create_input_model() -> Type[BaseModel]:
    return create_model(
        "PostDeleteInputModel",
        thread=(PositiveInt, ...),
        post=(PositiveInt, ...),
    )


async def validate_input_post_data(
    context: Context,
    validators: Dict[str, List[Validator]],
    data: PostDeleteInput,
    errors: ErrorsList,
) -> Tuple[PostDeleteInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def validate_input_thread_data(
    context: Context,
    validators: Dict[str, List[Validator]],
    data: PostDeleteInput,
    errors: ErrorsList,
) -> Tuple[PostDeleteInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def post_delete_action(context: Context, cleaned_data: PostDeleteInput) -> Thread:
    thread = cleaned_data["thread"]
    thread, last_post = await delete_thread_post(thread, cleaned_data["post"])

    posts_loader.unload(context, cleaned_data["post"].id)
    posts_loader.store(context, last_post)
    threads_loader.store(context, thread)

    return thread
