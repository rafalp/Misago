from typing import Optional

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ....categories.create import create_category
from ....categories.errors import CategoryInvalidParentError
from ....categories.get import get_all_categories
from ....categories.tree import insert_category
from ....types import Category
from ....validation import (
    CategoryExistsValidator,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler
from ..decorators import admin_mutation


create_category_mutation = MutationType()


@create_category_mutation.field("createCategory")
@error_handler
@admin_mutation
@convert_kwargs_to_snake_case
async def resolve_create_category(
    _, info: GraphQLResolveInfo, *, input: dict,  # pylint: disable=redefined-builtin
):
    categories = await get_all_categories()

    cleaned_data, errors = validate_model(CategoryInputModel, input)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {"parent": [CategoryExistsValidator(info.context), validate_parent]},
        errors,
    )

    if errors:
        return {"errors": errors}

    parent_obj: Optional[Category] = cleaned_data.get("parent")

    new_category = await create_category(
        name=cleaned_data["name"],
        parent=parent_obj,
        is_closed=cleaned_data.get("is_closed") or False,
    )
    new_category = await insert_category(categories, new_category, parent_obj)

    return {"category": new_category}


CategoryInputModel = create_model(
    "CategoryInputModel",
    name=(
        constr(strip_whitespace=True, min_length=1, max_length=255, regex=r"\w"),
        ...,
    ),
    parent=(Optional[PositiveInt], None),
    is_closed=(Optional[bool], False),
)


def validate_parent(parent: Category, *_) -> Category:
    if parent.depth > 0:
        raise CategoryInvalidParentError(category_id=parent.id)
    return parent
