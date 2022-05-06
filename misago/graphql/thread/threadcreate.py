from asyncio import gather
from typing import Dict, List, Optional, Tuple, Type

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model

from ...auth.errors import NotModeratorError
from ...auth.validators import IsAuthenticatedValidator
from ...categories.loaders import categories_loader
from ...categories.validators import CategoryExistsValidator, CategoryIsOpenValidator
from ...context import Context
from ...database import database
from ...pubsub.threads import publish_thread_update
from ...richtext import ParsedMarkupMetadata, parse_markup
from ...threads.loaders import posts_loader, threads_loader
from ...threads.models import Post, Thread
from ...threads.validators import threadtitlestr
from ...validation import ErrorsList, Validator, validate_data, validate_model
from ..mutation import ErrorType, MutationType
from .hooks.threadcreate import (
    ThreadCreateInput,
    thread_create_hook,
    thread_create_input_hook,
)
from .thread import ThreadType


class ThreadCreateInputType(InputType):
    __schema__ = gql(
        """
        input ThreadCreateInput {
            category: ID!
            title: String!
            markup: String!
            isClosed: Boolean
        }
        """
    )
    __args__ = {
        "isClosed": "is_closed",
    }


class ThreadCreateResultType(ObjectType):
    __schema__ = gql(
        """
        type ThreadCreateResult {
            thread: Thread
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, ThreadType]


class ThreadCreateMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            threadCreate(input: ThreadCreateInput!): ThreadCreateResult!
        }
        """
    )
    __requires__ = [ThreadCreateInputType, ThreadCreateResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        *,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        cleaned_data, errors = await cls.clean_data(info, input)

        if errors:
            return {"errors": errors}

        thread, _, _ = await thread_create_hook.call_action(
            cls.thread_create, info.context, cleaned_data
        )

        return {"thread": thread}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
        cleaned_data, errors = validate_model(input_model, data)

        if cleaned_data:
            validators: Dict[str, List[Validator]] = {
                "category": [
                    CategoryExistsValidator(info.context),
                    CategoryIsOpenValidator(info.context),
                ],
                ErrorsList.ROOT_LOCATION: [
                    IsAuthenticatedValidator(info.context),
                    IsClosedValidator(info.context),
                ],
            }

            cleaned_data, errors = await thread_create_input_hook.call_action(
                cls.validate_input_data, info.context, validators, cleaned_data, errors
            )

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
        return create_model(
            "ThreadCreateInputModel",
            category=(PositiveInt, ...),
            title=(threadtitlestr(context["settings"]), ...),
            markup=(
                constr(
                    strip_whitespace=True,
                    min_length=context["settings"]["post_min_length"],
                ),
                ...,
            ),
            is_closed=(Optional[bool], False),
        )

    @classmethod
    async def validate_input_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadCreateInput,
        errors: ErrorsList,
    ) -> Tuple[ThreadCreateInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def thread_create(
        cls, context: Context, cleaned_data: ThreadCreateInput
    ) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
        user = context["user"]
        rich_text, metadata = await parse_markup(context, cleaned_data["markup"])

        async with database.transaction():
            thread = await Thread.create(
                cleaned_data["category"],
                cleaned_data["title"],
                starter=user,
                is_closed=cleaned_data.get("is_closed") or False,
            )
            post = await Post.create(
                thread,
                cleaned_data["markup"],
                rich_text,
                poster=user,
            )
            category = cleaned_data["category"]
            thread, category = await gather(
                thread.update(first_post=post, last_post=post),
                category.update(increment_threads=True, increment_posts=True),
            )

        threads_loader.store(context, thread)
        categories_loader.store(context, category)
        posts_loader.store(context, post)

        await publish_thread_update(thread)

        return thread, post, metadata


class IsClosedValidator:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    def __call__(self, data: dict, errors: ErrorsList, *_) -> dict:
        user = self._context["user"]
        category = data.get("category")
        is_closed = data.get("is_closed")

        if category and is_closed and (not user or not user.is_moderator):
            errors.add_error("is_closed", NotModeratorError())

        return data
