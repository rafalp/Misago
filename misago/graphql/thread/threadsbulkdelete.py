from typing import Any, Dict, List, Tuple, Type

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ...auth.validators import IsAuthenticatedValidator
from ...categories.validators import CategoryModeratorValidator
from ...context import Context
from ...threads.loaders import posts_loader, threads_loader
from ...threads.models import Thread
from ...threads.validators import (
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
)
from ...validation import (
    ErrorsList,
    Validator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ..mutation import ErrorType, MutationType
from .hooks.threadsbulkdelete import (
    ThreadsBulkDeleteInput,
    threads_bulk_delete_hook,
    threads_bulk_delete_input_hook,
)


class ThreadsBulkDeleteResultType(ObjectType):
    __schema__ = gql(
        """
        type ThreadsBulkDeleteResult {
            deleted: [ID!]!
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType]


class ThreadsBulkDeleteMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            threadsBulkDelete(threads: [ID!]!): ThreadsBulkDeleteResult!
        }
        """
    )
    __requires__ = [ThreadsBulkDeleteResultType]

    @classmethod
    async def mutate(cls, info: GraphQLResolveInfo, **data):
        cleaned_data, errors = await cls.clean_data(info, data)

        result: Dict[str, Any] = {"deleted": []}

        if cls.is_valid(cleaned_data, errors):
            await threads_bulk_delete_hook.call_action(
                cls.threads_bulk_delete, info.context, cleaned_data
            )
            result["deleted"] = [i.id for i in cleaned_data["threads"]]

        if errors:
            result["errors"] = errors

        return result

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
        cleaned_data, errors = validate_model(input_model, data)

        if cleaned_data.get("threads"):
            # prime threads cache for bulk action
            await threads_loader.load_many(info.context, cleaned_data["threads"])

        if cleaned_data:
            validators: Dict[str, List[Validator]] = {
                "threads": [
                    ThreadsBulkValidator(
                        [
                            ThreadExistsValidator(info.context),
                            ThreadCategoryValidator(
                                info.context, CategoryModeratorValidator(info.context)
                            ),
                        ]
                    )
                ],
                ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
            }
            cleaned_data, errors = await threads_bulk_delete_input_hook.call_action(
                cls.validate_input_data, info.context, validators, cleaned_data, errors
            )

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
        return create_model(
            "ThreadsBulkDeleteInputModel",
            threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
        )

    @classmethod
    async def validate_input_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkDeleteInput,
        errors: ErrorsList,
    ) -> Tuple[ThreadsBulkDeleteInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    def is_valid(
        cls, cleaned_data: ThreadsBulkDeleteInput, errors_locations: ErrorsList
    ) -> bool:
        if errors_locations.has_root_errors:
            return False
        if not cleaned_data.get("threads"):
            return False
        return True

    @classmethod
    async def threads_bulk_delete(
        cls, context: Context, cleaned_data: ThreadsBulkDeleteInput
    ):
        threads_ids = [thread.id for thread in cleaned_data["threads"]]
        await Thread.query.filter(id__in=threads_ids).delete()

        threads_loader.unload_many(context, threads_ids)
        posts_loader.unload_with_thread_id_in(context, threads_ids)
