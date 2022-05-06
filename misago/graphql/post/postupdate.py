from typing import Dict, List, Tuple, Type, cast

from ariadne_graphql_modules import DeferredType, InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model

from ...auth.validators import IsAuthenticatedValidator
from ...categories.validators import CategoryIsOpenValidator
from ...context import Context
from ...richtext.parser import ParsedMarkupMetadata, parse_markup
from ...threads.loaders import posts_loader, threads_loader
from ...threads.models import Post, Thread
from ...threads.validators import (
    PostAuthorValidator,
    PostCategoryValidator,
    PostExistsValidator,
    PostThreadValidator,
    ThreadIsOpenValidator,
)
from ...validation import ErrorsList, Validator, validate_data, validate_model
from ..mutation import ErrorType, MutationType
from .hooks.postupdate import PostUpdateInput, post_update_hook, post_update_input_hook
from .post import PostType


class PostUpdateInputType(InputType):
    __schema__ = gql(
        """
        input PostUpdateInput {
            post: ID!
            markup: String!
        }
        """
    )


class PostUpdateResultType(ObjectType):
    __schema__ = gql(
        """
        type PostUpdateResult {
            updated: Boolean!
            thread: Thread
            post: Post
            errors: [Error!]
        }
        """
    )
    __requires__ = [DeferredType("Thread"), ErrorType, PostType]


class PostUpdateMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            postUpdate(input: PostUpdateInput!): PostUpdateResult!
        }
        """
    )
    __requires__ = [PostUpdateInputType, PostUpdateResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        *,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        cleaned_data, errors = await cls.clean_data(info, input)
        thread = cleaned_data.get("thread")
        post = cleaned_data.get("post")

        if errors:
            return {
                "errors": errors,
                "thread": thread,
                "post": post,
                "updated": False,
            }

        thread, updated_post, _ = await post_update_hook.call_action(
            cls.post_update, info.context, cleaned_data
        )

        return {
            "thread": thread,
            "post": updated_post,
            "updated": updated_post != post,
        }

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
        cleaned_data, errors = validate_model(input_model, data)

        post = None
        thread = None

        if cleaned_data.get("post"):
            post = await posts_loader.load(info.context, cleaned_data["post"])
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
                    PostThreadValidator(
                        info.context, ThreadIsOpenValidator(info.context)
                    ),
                ],
                ErrorsList.ROOT_LOCATION: [
                    IsAuthenticatedValidator(info.context),
                ],
            }
            cleaned_data, errors = await post_update_input_hook.call_action(
                cls.validate_input_data, info.context, validators, cleaned_data, errors
            )

        cleaned_data["thread"] = thread
        cleaned_data["post"] = post

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
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

    @classmethod
    async def validate_input_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: PostUpdateInput,
        errors: ErrorsList,
    ) -> Tuple[PostUpdateInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def post_update(
        cls, context: Context, cleaned_data: PostUpdateInput
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
