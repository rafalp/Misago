from typing import Optional, Type, cast

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model

from ...categories.get import get_all_categories
from ...categories.models import Category
from ...categories.tree import move_category
from ...categories.validators import CategoryExistsValidator, validate_category_parent
from ...validation import (
    ROOT_LOCATION,
    color_validator,
    root_validator,
    validate_data,
    validate_model,
)
from ..mutation import AdminMutationType, ErrorType
from .category import AdminCategoryType
from .categorycreate import CategoryCreateInputModel


class AdminCategoryUpdateInputType(InputType):
    __schema__ = gql(
        """
        input CategoryUpdateInput {
            name: String
            color: String
            icon: String
            parent: ID
            isClosed: Boolean
        }
        """
    )
    __args__ = {
        "isClosed": "is_closed",
    }


class AdminCategoryUpdateResultType(ObjectType):
    __schema__ = gql(
        """
        type CategoryUpdateResult {
            category: Category
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, AdminCategoryType]


class AdminCategoryUpdateMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            categoryUpdate(
                category: ID!, input: CategoryUpdateInput!
            ): CategoryUpdateResult!
        }
        """
    )
    __requires__ = [AdminCategoryUpdateInputType, AdminCategoryUpdateResultType]

    @classmethod
    async def mutate(
        cls,
        info: GraphQLResolveInfo,
        *,
        category: str,
        input: dict,  # pylint: disable=redefined-builtin
    ):
        input["category"] = category
        cleaned_data, errors = await cls.clean_data(info, input)
        category_obj = cast(Optional[Category], cleaned_data.pop("category", None))
        if errors or not category_obj:
            return {"errors": errors, "updated": False, "category": category_obj}

        new_parent = cast(Optional[Category], cleaned_data.pop("parent", None))

        updated_category = await category_obj.update(**cleaned_data)

        if "parent" in input:
            parent_id = new_parent.id if new_parent else None

            if updated_category.parent_id != parent_id:
                categories = await get_all_categories()
                updated_category, _ = await move_category(
                    categories, updated_category, parent=new_parent
                )

        return {
            "updated": updated_category != category_obj,
            "category": updated_category,
        }

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        cleaned_data, errors = validate_model(CategoryUpdateInputModel, data)
        cleaned_data, errors = await validate_data(
            cleaned_data,
            {
                "category": [CategoryExistsValidator(info.context)],
                "color": [color_validator],
                "parent": [
                    CategoryExistsValidator(info.context),
                ],
                ROOT_LOCATION: [validate_parent_value],
            },
            errors,
        )
        return cleaned_data, errors


CategoryUpdateInputModel: Type[BaseModel] = create_model(
    "CategoryUpdateInputModel",
    __base__=CategoryCreateInputModel,
    category=(PositiveInt, ...),
    name=(
        constr(strip_whitespace=True, min_length=1, max_length=255, regex=r"\w"),
        None,
    ),
)


@root_validator(location="parent")
def validate_parent_value(cleaned_data: dict, *_) -> dict:
    if "category" not in cleaned_data:
        return cleaned_data

    if "parent" in cleaned_data:
        validate_category_parent(cleaned_data["category"], cleaned_data["parent"])

    return cleaned_data
