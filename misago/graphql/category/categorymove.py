from typing import Optional, Type

from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ...categories.errors import CategoryInvalidParentError
from ...categories.get import get_all_categories
from ...categories.loaders import categories_loader
from ...categories.models import Category
from ...categories.tree import move_category
from ...categories.validators import CategoryExistsValidator
from ...validation import ROOT_LOCATION, root_validator, validate_data, validate_model
from ..mutation import AdminMutationType, ErrorType
from .category import AdminCategoryType
from .categoryupdate import validate_parent_value


class AdminCategoryMoveResultType(ObjectType):
    __schema__ = gql(
        """
        type CategoryMoveResult {
            category: Category
            categories: [Category!]!
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, AdminCategoryType]


class AdminCategoryMoveMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            categoryMove(category: ID!, parent: ID, before: ID): CategoryMoveResult!
        }
        """
    )
    __requires__ = [AdminCategoryMoveResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        *,
        category: str,
        parent: Optional[str] = None,
        before: Optional[str] = None,
    ):
        categories = await get_all_categories()

        cleaned_data, errors = await cls.clean_data(
            info,
            {
                "category": category,
                "parent": parent,
                "before": before,
            },
        )

        category_obj: Optional[Category] = cleaned_data.get("category")

        if errors or not category_obj:
            return {
                "errors": errors,
                "category": category_obj,
                "categories": categories,
            }

        category_obj, updated_categories = await move_category(
            categories,
            category_obj,
            parent=cleaned_data.get("parent"),
            before=cleaned_data.get("before"),
        )

        categories_loader.unload_all(info.context)

        return {"category": category_obj, "categories": updated_categories}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        cleaned_data, errors = validate_model(MoveCategoryInputModel, data)
        cleaned_data, errors = await validate_data(
            cleaned_data,
            {
                "category": [CategoryExistsValidator(info.context)],
                "parent": [CategoryExistsValidator(info.context)],
                "before": [CategoryExistsValidator(info.context)],
                ROOT_LOCATION: [validate_parent_value, validate_before_value],
            },
            errors,
        )
        return cleaned_data, errors


MoveCategoryInputModel: Type[BaseModel] = create_model(
    "MoveCategoryInputModel",
    category=(
        PositiveInt,
        ...,
    ),
    parent=(Optional[PositiveInt], None),
    before=(Optional[PositiveInt], None),
)


@root_validator(location="before")
def validate_before_value(cleaned_data: dict, *_) -> dict:
    if (
        "category" not in cleaned_data
        or "parent" not in cleaned_data
        or "before" not in cleaned_data
    ):
        return cleaned_data

    category: Category = cleaned_data["category"]
    parent: Optional[Category] = cleaned_data["parent"]
    before: Optional[Category] = cleaned_data["before"]

    if before and before.id == category.id:
        raise CategoryInvalidParentError(category_id=before.id)

    parent_id = parent.id if parent else None
    if before and before.parent_id != parent_id:
        raise CategoryInvalidParentError(category_id=before.id)

    return cleaned_data
