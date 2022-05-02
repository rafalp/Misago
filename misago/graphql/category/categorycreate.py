from typing import Optional, Type

from ariadne_graphql_modules import InputType, ObjectType, gql
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model
from pydantic.color import Color

from ...categories.errors import CategoryInvalidParentError
from ...categories.get import get_all_categories
from ...categories.models import Category
from ...categories.tree import insert_category
from ...categories.validators import CategoryExistsValidator
from ...validation import color_validator, validate_data, validate_model
from ..mutation import AdminMutationType, ErrorType
from .category import AdminCategoryType


class AdminCategoryCreateInputType(InputType):
    __schema__ = gql(
        """
        input CategoryCreateInput {
            name: String!
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


class AdminCategoryCreateResultType(ObjectType):
    __schema__ = gql(
        """
        type CategoryCreateResult {
            category: Category
            errors: [Error!]
        }
        """
    )
    __requires__ = [ErrorType, AdminCategoryType]


class AdminCategoryCreateMutation(AdminMutationType):
    __schema__ = gql(
        """
        type Mutation {
            categoryCreate(input: CategoryCreateInput!): CategoryCreateResult!
        }
        """
    )
    __requires__ = [AdminCategoryCreateInputType, AdminCategoryCreateResultType]

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

        categories = await get_all_categories()
        parent: Optional[Category] = cleaned_data.get("parent")

        category_obj = await Category.create(
            name=cleaned_data["name"],
            color=cleaned_data["color"],
            icon=cleaned_data["icon"],
            parent=parent,
            is_closed=cleaned_data.get("is_closed") or False,
        )
        category_obj, _ = await insert_category(categories, category_obj, parent)

        return {"category": category_obj}

    @classmethod
    async def clean_data(cls, info: GraphQLResolveInfo, data: dict):
        cleaned_data, errors = validate_model(CategoryCreateInputModel, data)
        cleaned_data, errors = await validate_data(
            cleaned_data,
            {
                "color": [color_validator],
                "parent": [CategoryExistsValidator(info.context), validate_parent],
            },
            errors,
        )
        return cleaned_data, errors


CategoryCreateInputModel: Type[BaseModel] = create_model(
    "CategoryCreateInputModel",
    name=(
        constr(strip_whitespace=True, min_length=1, max_length=255, regex=r"\w"),
        ...,
    ),
    color=(Color, None),
    icon=(constr(strip_whitespace=True, min_length=0, max_length=255), None),
    parent=(Optional[PositiveInt], None),
    is_closed=(Optional[bool], False),
)


def validate_parent(parent: Category, *_) -> Category:
    if parent.depth > 0:
        raise CategoryInvalidParentError(category_id=parent.id)
    return parent
