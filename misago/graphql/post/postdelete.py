from typing import Dict, List, Tuple, Type

from ariadne_graphql_modules import DeferredType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ...auth.validators import IsAuthenticatedValidator
from ...categories.validators import CategoryModeratorValidator
from ...context import Context
from ...threads.delete import delete_thread_post
from ...threads.loaders import posts_loader, threads_loader
from ...threads.models import Thread
from ...threads.validators import (
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadPostExistsValidator,
    ThreadPostIsReplyValidator,
)
from ...validation import ErrorsList, Validator, validate_data, validate_model
from ..mutation import ErrorType, MutationType
from .hooks.postdelete import (
    PostDeleteInput,
    post_delete_hook,
    post_delete_input_post_hook,
    post_delete_input_thread_hook,
)
from .post import PostType
from .postspage import PostsPageType
from .resolvers import resolve_posts_page


class PostDeleteResultType(ObjectType):
    __schema__ = gql(
        """
        type PostDeleteResult {
            deleted: Boolean!
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


class PostDeleteMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            postDelete(thread: ID!, post: ID!): PostDeleteResult!
        }
        """
    )
    __requires__ = [PostDeleteResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        **data,
    ):
        cleaned_data, errors = await cls.clean_data(info, data)
        thread = cleaned_data.get("org_thread")

        if errors:
            return {"errors": errors, "thread": thread, "deleted": False}

        thread = await post_delete_hook.call_action(
            cls.post_delete, info.context, cleaned_data
        )

        return {"thread": thread, "deleted": True}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model()
        cleaned_data, errors = validate_model(input_model, data)

        if cleaned_data.get("thread"):
            cleaned_data["org_thread"] = await threads_loader.load(
                info.context, cleaned_data["thread"]
            )

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
                cls.validate_input_thread_data,
                info.context,
                thread_validators,
                cleaned_data,
                errors,
            )

        if errors:
            return cleaned_data, errors

        if cleaned_data.get("thread"):
            post_validators: Dict[str, List[Validator]] = {
                "post": [
                    ThreadPostExistsValidator(info.context, cleaned_data["thread"]),
                    ThreadPostIsReplyValidator(cleaned_data["thread"]),
                ],
            }
            cleaned_data, errors = await post_delete_input_post_hook.call_action(
                cls.validate_input_post_data,
                info.context,
                post_validators,
                cleaned_data,
                errors,
            )

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls) -> Type[BaseModel]:
        return create_model(
            "PostDeleteInputModel",
            thread=(PositiveInt, ...),
            post=(PositiveInt, ...),
        )

    @classmethod
    async def validate_input_post_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: PostDeleteInput,
        errors: ErrorsList,
    ) -> Tuple[PostDeleteInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def validate_input_thread_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: PostDeleteInput,
        errors: ErrorsList,
    ) -> Tuple[PostDeleteInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def post_delete(
        cls, context: Context, cleaned_data: PostDeleteInput
    ) -> Thread:
        thread = cleaned_data["thread"]
        thread, last_post = await delete_thread_post(thread, cleaned_data["post"])

        posts_loader.unload(context, cleaned_data["post"].id)
        posts_loader.store(context, last_post)
        threads_loader.store(context, thread)

        return thread
