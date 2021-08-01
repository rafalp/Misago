from typing import Optional, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model
from pydantic.color import Color

from ....categories.errors import CategoryInvalidParentError
from ....categories.get import get_all_categories
from ....categories.models import Category
from ....categories.tree import insert_category
from ....validation import (
    CategoryExistsValidator,
    color_validator,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler
from ..decorators import admin_resolver

category_create_mutation = MutationType()


@category_create_mutation.field("categoryCreate")
@admin_resolver
@error_handler
@convert_kwargs_to_snake_case
async def resolve_category_create(
    _,
    info: GraphQLResolveInfo,
    *,
    input: dict,  # pylint: disable=redefined-builtin
):
    categories = await get_all_categories()

    cleaned_data, errors = validate_model(CategoryCreateInputModel, input)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {
            "color": [color_validator],
            "parent": [CategoryExistsValidator(info.context), validate_parent],
        },
        errors,
    )

    if errors:
        return {"errors": errors}

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
