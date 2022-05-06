from typing import Dict, List, Tuple, Type

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ...auth.validators import IsAuthenticatedValidator
from ...categories.validators import CategoryIsOpenValidator
from ...context import Context
from ...threads.loaders import threads_loader
from ...threads.models import Thread
from ...threads.validators import (
    ThreadAuthorValidator,
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadIsOpenValidator,
    threadtitlestr,
)
from ...validation import ErrorsList, Validator, validate_data, validate_model
from ..mutation import ErrorType, MutationType
from .hooks.threadrename import (
    ThreadRenameInput,
    thread_rename_hook,
    thread_rename_input_hook,
)
from .thread import ThreadType


class ThreadRenameResultType(ObjectType):
    __schema__ = gql(
        """
        type ThreadRenameResult {
            updated: Boolean!
            thread: Thread
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, ThreadType]


class ThreadRenameMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            threadRename(thread: ID!, title: String!): ThreadRenameResult!
        }
        """
    )
    __requires__ = [ThreadRenameResultType]

    @classmethod
    async def mutate(cls, info: GraphQLResolveInfo, **data):
        cleaned_data, errors = await cls.clean_data(info, data)
        thread = cleaned_data.get("org_thread")

        if errors:
            return {"errors": errors, "thread": thread, "updated": False}

        updated_thread = await thread_rename_hook.call_action(
            cls.thread_rename, info.context, cleaned_data
        )

        return {"thread": updated_thread, "updated": updated_thread != thread}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
        cleaned_data, errors = validate_model(input_model, data)

        if cleaned_data.get("thread"):
            cleaned_data["org_thread"] = await threads_loader.load(
                info.context, cleaned_data["thread"]
            )

        if cleaned_data:
            validators: Dict[str, List[Validator]] = {
                "thread": [
                    ThreadExistsValidator(info.context),
                    ThreadAuthorValidator(info.context),
                    ThreadCategoryValidator(
                        info.context, CategoryIsOpenValidator(info.context)
                    ),
                    ThreadIsOpenValidator(info.context),
                ],
                ErrorsList.ROOT_LOCATION: [
                    IsAuthenticatedValidator(info.context),
                ],
            }
            cleaned_data, errors = await thread_rename_input_hook.call_action(
                cls.validate_input_data, info.context, validators, cleaned_data, errors
            )

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
        return create_model(
            "ThreadRenameInputModel",
            thread=(PositiveInt, ...),
            title=(threadtitlestr(context["settings"]), ...),
        )

    @classmethod
    async def validate_input_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadRenameInput,
        errors: ErrorsList,
    ) -> Tuple[ThreadRenameInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def thread_rename(
        cls, context: Context, cleaned_data: ThreadRenameInput
    ) -> Thread:
        thread = cleaned_data["thread"]
        thread = await thread.update(title=cleaned_data["title"])

        threads_loader.store(context, thread)

        return thread
