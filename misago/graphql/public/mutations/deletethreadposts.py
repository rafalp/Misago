from typing import Dict, List, Tuple

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....errors import ErrorsList
from ....hooks import (
    delete_thread_posts_hook,
    delete_thread_posts_input_model_hook,
    delete_thread_posts_input_posts_hook,
    delete_thread_posts_input_thread_hook,
)
from ....loaders import clear_posts, load_posts, load_thread, store_post, store_thread
from ....threads.delete import delete_thread_posts
from ....types import (
    DeleteThreadPostsInput,
    DeleteThreadPostsInputModel,
    GraphQLContext,
    Thread,
    Validator,
)
from ....validation import (
    ROOT_LOCATION,
    CategoryModeratorValidator,
    PostsBulkValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadPostExistsValidator,
    ThreadPostIsReplyValidator,
    UserIsAuthorizedRootValidator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler

delete_thread_posts_mutation = MutationType()


@delete_thread_posts_mutation.field("deleteThreadPosts")
@convert_kwargs_to_snake_case
@error_handler
async def resolve_delete_thread_posts(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    input_model = await delete_thread_posts_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data.get("thread"):
        thread = await load_thread(info.context, cleaned_data["thread"])
    else:
        thread = None

    if thread and cleaned_data.get("posts"):
        # prime posts cache for bulk action
        await load_posts(info.context, cleaned_data["posts"])

    if cleaned_data:
        thread_validators: Dict[str, List[Validator]] = {
            "thread": [
                ThreadExistsValidator(info.context),
                ThreadCategoryValidator(
                    info.context, CategoryModeratorValidator(info.context)
                ),
            ],
            ROOT_LOCATION: [UserIsAuthorizedRootValidator(info.context)],
        }

        (
            cleaned_data,
            errors,
        ) = await delete_thread_posts_input_thread_hook.call_action(
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
            "thread": cleaned_data.get("thread"),
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

        (
            cleaned_data,
            errors,
        ) = await delete_thread_posts_input_posts_hook.call_action(
            validate_input_posts_data,
            info.context,
            posts_validators,
            cleaned_data,
            errors,
        )

    if cleaned_data.get("posts"):
        deleted = [i.id for i in cleaned_data["posts"]]
        thread = await delete_thread_posts_hook.call_action(
            delete_thread_posts_action, info.context, cleaned_data
        )

    if errors:
        return {
            "errors": errors,
            "thread": thread,
            "deleted": deleted,
        }

    return {"thread": thread, "deleted": deleted}


async def create_input_model(context: GraphQLContext) -> DeleteThreadPostsInputModel:
    return create_model(
        "DeleteThreadPostsInputModel",
        thread=(PositiveInt, ...),
        posts=(bulkactionidslist(PositiveInt, context["settings"]), ...),
    )


async def validate_input_posts_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: DeleteThreadPostsInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadPostsInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def validate_input_thread_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: DeleteThreadPostsInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadPostsInput, ErrorsList]:
    return await validate_data(data, validators, errors)


async def delete_thread_posts_action(
    context: GraphQLContext, cleaned_data: DeleteThreadPostsInput
) -> Thread:
    thread = cleaned_data["thread"]
    thread, last_post = await delete_thread_posts(thread, cleaned_data["posts"])
    clear_posts(context, cleaned_data["posts"])
    store_post(context, last_post)
    store_thread(context, thread)
    return thread
