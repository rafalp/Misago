from typing import Dict, List, Tuple, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....auth.validators import IsAuthenticatedValidator
from ....categories.validators import CategoryModeratorValidator
from ....context import Context
from ....threads.delete import delete_thread_posts
from ....threads.loaders import posts_loader, threads_loader
from ....threads.models import Thread
from ....threads.validators import (
    PostsBulkValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadPostExistsValidator,
    ThreadPostIsReplyValidator,
)
from ....validation import (
    ROOT_LOCATION,
    ErrorsList,
    Validator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler
from .hooks.postsbulkdelete import (
    PostsBulkDeleteInput,
    posts_bulk_delete_hook,
    posts_bulk_delete_input_posts_hook,
    posts_bulk_delete_input_thread_hook,
)

posts_bulk_delete_mutation = MutationType()


@posts_bulk_delete_mutation.field("postsBulkDelete")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_posts_bulk_delete(
    _, info: GraphQLResolveInfo, **input  # pylint: disable=redefined-builtin
):
    input_model = create_input_model(info.context)
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await threads_loader.load(info.context, cleaned_data["thread"])
    else:
        thread = None

    if thread and cleaned_data.get("posts"):
        # prime posts cache for bulk action
        await posts_loader.load_many(info.context, cleaned_data["posts"])

    if cleaned_data:
        thread_validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
        }

        cleaned_data, errors = await posts_bulk_delete_input_thread_hook.call_action(
            validate_input_thread_data,
            info.context,
            thread_validators,
            cleaned_data,
            errors,
        )

    deleted: List[str] = []

    if errors:
        return {
            "errors": errors,
            "thread": thread,
            "deleted": deleted,
        }

    if cleaned_data.get("thread"):
        posts_validators: Dict[str, List[Validator]] = {
            "posts": [
                PostsBulkValidator(
                    [
                        ThreadPostExistsValidator(info.context, cleaned_data["thread"]),
                        ThreadPostIsReplyValidator(cleaned_data["thread"]),
                    ]
                )
            ],
        }

        cleaned_data, errors = await posts_bulk_delete_input_posts_hook.call_action(
            validate_input_posts_data,
            info.context,
            posts_validators,
            cleaned_data,
            errors,
        )

    if cleaned_data.get("posts"):
        deleted = [i.id for i in cleaned_data["posts"]]
        thread = await posts_bulk_delete_hook.call_action(
            posts_bulk_delete_action, info.context, cleaned_data
        )

    if errors:
        return {
            "errors": errors,
            "thread": thread,
            "deleted": deleted,
        }

    return {"thread": thread, "deleted": deleted}


def create_input_model(context: Context) -> Type[BaseModel]:
    return create_model(
        "PostsBulkDeleteInputModel",
        thread=(PositiveInt, ...),
        posts=(bulkactionidslist(PositiveInt, context["settings"]), ...),
    )


async def validate_input_posts_data(
    context: Context,
    validators: Dict[str, List[Validator]],
    data: PostsBulkDeleteInput,
    errors: ErrorsList,
) -> Tuple[PostsBulkDeleteInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def validate_input_thread_data(
    context: Context,
    validators: Dict[str, List[Validator]],
    data: PostsBulkDeleteInput,
    errors: ErrorsList,
) -> Tuple[PostsBulkDeleteInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def posts_bulk_delete_action(
    context: Context, cleaned_data: PostsBulkDeleteInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread, last_post = await delete_thread_posts(thread, cleaned_data["posts"])

    posts_loader.unload_many(context, [post.id for post in cleaned_data["posts"]])
    posts_loader.store(context, last_post)
    threads_loader.store(context, thread)

    return thread