from typing import Optional

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....categories.errors import CategoryInvalidParentError
from ....categories.get import get_all_categories
from ....categories.tree import move_category
from ....loaders import clear_categories
from ....types import Category
from ....validation import (
    ROOT_LOCATION,
    CategoryExistsValidator,
    for_location,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler
from ..decorators import admin_mutation
from .editcategory import validate_parent_value

move_category_mutation = MutationType()


@move_category_mutation.field("moveCategory")
@error_handler
@admin_mutation
@convert_kwargs_to_snake_case
async def resolve_move_category(
    _,
    info: GraphQLResolveInfo,
    *,
    category: str,
    parent: Optional[str] = None,
    before: Optional[str] = None
):
    categories = await get_all_categories()
    root_categories = [c for c in categories if c.depth == 0]

    cleaned_data, errors = validate_model(
        MoveCategoryInputModel,
        {"category": category, "parent": parent, "before": before},
    )
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

    category_obj: Optional[Category] = cleaned_data.get("category")

    if errors or not category_obj:
        return {
            "errors": errors,
            "category": category_obj,
            "categories": root_categories,
        }

    moved_category, updated_categories = await move_category(
        categories,
        category_obj,
        parent=cleaned_data.get("parent"),
        before=cleaned_data.get("before"),
    )

    clear_categories(info.context)

    root_categories = [c for c in updated_categories if c.depth == 0]
    return {"category": moved_category, "categories": root_categories}


MoveCategoryInputModel = create_model(
    "MoveCategoryInputModel",
    category=(PositiveInt, ...,),
    parent=(Optional[PositiveInt], None),
    before=(Optional[PositiveInt], None),
)


@for_location("before")
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
