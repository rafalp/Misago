from typing import Optional, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt

from ....categories.errors import CategoryInvalidParentError
from ....categories.get import get_all_categories
from ....categories.tree import move_category
from ....categories.update import update_category
from ....categories.validators import validate_category_parent
from ....errors import ErrorsList
from ....types import Category
from ....validation import (
    ROOT_LOCATION,
    CategoryExistsValidator,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler
from ..decorators import admin_mutation
from .createcategory import CategoryInputModel

edit_category_mutation = MutationType()


@edit_category_mutation.field("editCategory")
@error_handler
@admin_mutation
@convert_kwargs_to_snake_case
async def resolve_edit_category(
    _,
    info: GraphQLResolveInfo,
    *,
    category: str,
    input: dict,  # pylint: disable=redefined-builtin
):
    input["category"] = category

    cleaned_data, errors = validate_model(EditCategoryInputModel, input)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {
            "category": [CategoryExistsValidator(info.context)],
            "parent": [CategoryExistsValidator(info.context),],
            ROOT_LOCATION: [validate_parent_value],
        },
        errors,
    )

    category_obj = cast(Optional[Category], cleaned_data.get("category"))
    if errors or not category_obj:
        return {"errors": errors, "category": category_obj}

    updated_category = await update_category(
        category_obj,
        name=cleaned_data["name"],
        is_closed=cleaned_data.get("is_closed") or False,
    )

    parent = cast(Optional[Category], cleaned_data.get("parent"))
    parent_id = parent.id if parent else None

    if updated_category.parent_id != parent_id:
        categories = await get_all_categories()
        updated_category = await move_category(
            categories, updated_category, parent=parent
        )

    return {"category": updated_category}


class EditCategoryInputModel(CategoryInputModel):  # type: ignore
    category: PositiveInt


def validate_parent_value(cleaned_data: dict, errors: ErrorsList, *_) -> dict:
    if "category" not in cleaned_data:
        return cleaned_data

    if "parent" in cleaned_data:
        try:
            validate_category_parent(cleaned_data["category"], cleaned_data["parent"])
        except CategoryInvalidParentError as e:
            cleaned_data.pop("parent")
            errors.add_error("parent", e)

    return cleaned_data
