from typing import Dict, List, Tuple, Type

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ...auth.validators import IsAuthenticatedValidator
from ...categories.validators import (
    CategoryExistsValidator,
    CategoryIsOpenValidator,
    CategoryModeratorValidator,
)
from ...context import Context
from ...threads.loaders import posts_loader, threads_loader
from ...threads.models import Thread
from ...threads.move import move_threads
from ...threads.validators import (
    ThreadCategoryValidator,
    ThreadExistsValidator,
    ThreadsBulkValidator,
)
from ...utils.lists import remove_none_items, update_list_items
from ...validation import (
    ErrorsList,
    Validator,
    bulkactionidslist,
    validate_data,
    validate_model,
)
from ..mutation import ErrorType, MutationType
from .hooks.threadsbulkmove import (
    ThreadsBulkMoveInput,
    threads_bulk_move_hook,
    threads_bulk_move_input_hook,
)
from .thread import ThreadType


class ThreadsBulkMoveResultType(ObjectType):
    __schema__ = gql(
        """
        type ThreadsBulkMoveResult {
            updated: [ID!]!
            threads: [Thread!]
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, ThreadType]


class ThreadsBulkMoveMutation(MutationType):
    __schema__ = gql(
        """
        type Mutation {
            threadsBulkMove(threads: [ID!]!, category: ID!): ThreadsBulkMoveResult!
        }
        """
    )
    __requires__ = [ThreadsBulkMoveResultType]

    @classmethod
    async def mutate(cls, info: GraphQLResolveInfo, **data):
        cleaned_data, errors = await cls.clean_data(info, data)
        threads = cleaned_data.get("org_threads") or []

        if cls.is_valid(cleaned_data, errors):
            updated_threads = await threads_bulk_move_hook.call_action(
                cls.threads_bulk_move, info.context, cleaned_data
            )

            result = {
                "threads": update_list_items(threads, updated_threads),
                "updated": sorted([thread.id for thread in updated_threads]),
            }
        else:
            result = {"threads": threads, "updated": []}

        if errors:
            result["errors"] = errors

        return result

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        input_model = cls.create_input_model(info.context)
        cleaned_data, errors = validate_model(input_model, data)

        if cleaned_data.get("threads"):
            cleaned_data["org_threads"] = remove_none_items(
                await threads_loader.load_many(info.context, cleaned_data["threads"])
            )

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
                "category": [
                    CategoryExistsValidator(info.context),
                    CategoryIsOpenValidator(info.context),
                ],
                ErrorsList.ROOT_LOCATION: [IsAuthenticatedValidator(info.context)],
            }
            cleaned_data, errors = await threads_bulk_move_input_hook.call_action(
                cls.validate_input_data, info.context, validators, cleaned_data, errors
            )

        return cleaned_data, errors

    @classmethod
    def create_input_model(cls, context: Context) -> Type[BaseModel]:
        return create_model(
            "ThreadsBulkMoveInputModel",
            threads=(bulkactionidslist(PositiveInt, context["settings"]), ...),
            category=(PositiveInt, ...),
        )

    @classmethod
    async def validate_input_data(
        cls,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkMoveInput,
        errors: ErrorsList,
    ) -> Tuple[ThreadsBulkMoveInput, ErrorsList]:
        return await validate_data(data, validators, errors)

    @classmethod
    def is_valid(
        cls, cleaned_data: ThreadsBulkMoveInput, errors_locations: ErrorsList
    ) -> bool:
        if errors_locations.has_root_errors:
            return False
        if not cleaned_data.get("category") or not cleaned_data.get("threads"):
            return False
        return True

    @classmethod
    async def threads_bulk_move(
        cls, context: Context, cleaned_data: ThreadsBulkMoveInput
    ):
        threads = cleaned_data["threads"]
        threads = await move_threads(threads, cleaned_data["category"])

        threads_loader.store_many(context, threads)
        posts_loader.unload_with_thread_id_in(
            context, [thread.id for thread in threads]
        )

        return threads
