from typing import Dict, List, Tuple, Type

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ...auth.validators import IsAuthenticatedValidator
from ...categories.validators import CategoryModeratorValidator
from ...context import Context
from ...threads.loaders import posts_loader, threads_loader
from ...threads.validators import ThreadCategoryValidator, ThreadExistsValidator
from ...validation import ErrorsList, Validator, validate_data, validate_model
from ..mutation import ErrorType, MutationType
from .hooks.threaddelete import (
    ThreadDeleteInput,
    thread_delete_hook,
    thread_delete_input_hook,
)


class ThreadDeleteResultType(ObjectType):
    __schema__ = gql(
        """
        type ThreadDeleteResult {
            deleted: Boolean!
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType]


class ThreadDeleteMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            threadDelete(thread: ID!): ThreadDeleteResult!
        }
        """
    )
    __requires__ = [ThreadDeleteResultType]

    @classmethod
    async def mutate(cls, info: GraphQLResolveInfo, **data):
        cleaned_data, errors = await cls.clean_data(info, data)

        if errors:
            return {"errors": errors, "deleted": False}

        await thread_delete_hook.call_action(
            cls.thread_delete, info.context, cleaned_data
        )

        return {"deleted": True}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model()
        cleaned_data, errors = validate_model(input_model, data)

        if cleaned_data:
            validators: Dict[str, List[Validator]] = {
                "thread": [
                    ThreadExistsValidator(info.context),
                    ThreadCategoryValidator(
                        info.context, CategoryModeratorValidator(info.context)
                    ),
                ],
                ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
            }
            cleaned_data, errors = await thread_delete_input_hook.call_action(
                cls.validate_input_data, info.context, validators, cleaned_data, errors
            )

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls) -> Type[BaseModel]:
        return create_model("ThreadDeleteInputModel", thread=(PositiveInt, ...))

    @classmethod
    async def validate_input_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadDeleteInput,
        errors: ErrorsList,
    ) -> Tuple[ThreadDeleteInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    async def thread_delete(cls, context: Context, cleaned_data: ThreadDeleteInput):
        thread = cleaned_data["thread"]
        await thread.delete()

        threads_loader.unload(context, thread.id)
        posts_loader.unload_with_thread_id(context, thread.id)
