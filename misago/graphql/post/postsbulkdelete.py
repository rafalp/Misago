from typing import Dict, List, Tuple, Type

from ariadne_graphql_modules import DeferredType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ...auth.validators import IsAuthenticatedValidator
from ...categories.validators import CategoryModeratorValidator
from ...context import Context
from ...threads.delete import delete_thread_posts
from ...threads.loaders import posts_loader, threads_loader
from ...threads.models import Thread
from ...threads.validators import (
    PostsBulkValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadPostExistsValidator,
    ThreadPostIsReplyValidator,
)
from ...validation import (
    ROOT_LOCATION,
    ErrorsList,
    Validator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ..mutation import ErrorType, MutationType
from .hooks.postsbulkdelete import (
    PostsBulkDeleteInput,
    posts_bulk_delete_hook,
    posts_bulk_delete_input_posts_hook,
    posts_bulk_delete_input_thread_hook,
)
from .post import PostType
from .postspage import PostsPageType
from .resolvers import resolve_posts_page


class PostsBulkDeleteResultType(ObjectType):
    __schema__ = gql(
        """
        type PostsBulkDeleteResult {
            deleted: [ID!]!
            thread: Thread
            posts(page: Int): PostsPage
            errors: [Error!]
        }
        """
    )
    __requires__ = [
        DeferredType("Thread"),
        ErrorType,
        PostsPageType,
        PostType,
    ]

    @staticmethod
    def resolve_posts(result: dict, info: GraphQLResolveInfo, *, page: int = 1):
        if result.get("thread"):
            return resolve_posts_page(info, result["thread"].id, page=page)

        return None


class PostsBulkDeleteMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            postsBulkDelete(thread: ID!, posts: [ID!]!): PostsBulkDeleteResult!
        }
        """
    )
    __requires__ = [PostsBulkDeleteResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        **data,
    ):
        cleaned_data, errors = await cls.clean_data(info, data)

        deleted: List[str] = []
        thread = cleaned_data.get("thread")

        if cleaned_data.get("posts"):
            deleted = [i.id for i in cleaned_data["posts"]]
            thread = await posts_bulk_delete_hook.call_action(
                cls.posts_bulk_delete_action, info.context, cleaned_data
            )

        if errors:
            return {
                "errors": errors,
                "thread": thread,
                "deleted": deleted,
            }

        return {"thread": thread, "deleted": deleted}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
        cleaned_data, errors = validate_model(input_model, data)

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

            (
                cleaned_data,
                errors,
            ) = await posts_bulk_delete_input_thread_hook.call_action(
                cls.validate_input_thread_data,
                info.context,
                thread_validators,
                cleaned_data,
                errors,
            )

        if cleaned_data.get("thread"):
            posts_validators: Dict[str, List[Validator]] = {
                "posts": [
                    PostsBulkValidator(
                        [
                            ThreadPostExistsValidator(
                                info.context, cleaned_data["thread"]
                            ),
                            ThreadPostIsReplyValidator(cleaned_data["thread"]),
                        ]
                    )
                ],
            }

            cleaned_data, errors = await posts_bulk_delete_input_posts_hook.call_action(
                cls.validate_input_posts_data,
                info.context,
                posts_validators,
                cleaned_data,
                errors,
            )
        else:
            # Remove partially validated posts list
            cleaned_data.pop("posts", None)

        cleaned_data["thread"] = thread
        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
        return create_model(
            "PostsBulkDeleteInputModel",
            thread=(PositiveInt, ...),
            posts=(bulkactionidslist(PositiveInt, context["settings"]), ...),
        )

    @classmethod
    async def validate_input_posts_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: PostsBulkDeleteInput,
        errors: ErrorsList,
    ) -> Tuple[PostsBulkDeleteInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def validate_input_thread_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: PostsBulkDeleteInput,
        errors: ErrorsList,
    ) -> Tuple[PostsBulkDeleteInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def posts_bulk_delete_action(
        cls, context: Context, cleaned_data: PostsBulkDeleteInput
    ) -> Thread:
        thread = cleaned_data["thread"]
        thread, last_post = await delete_thread_posts(thread, cleaned_data["posts"])

        posts_loader.unload_many(context, [post.id for post in cleaned_data["posts"]])
        posts_loader.store(context, last_post)
        threads_loader.store(context, thread)

        return thread
