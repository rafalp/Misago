from typing import Optional, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt

from ....categories.get import get_all_categories
from ....categories.tree import move_category
from ....categories.update import update_category
from ....types import Category
from ....validation import (
    CategoryExistsValidator,
    CategoryParentValidator,
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
        },
        errors,
    )

    category_obj = cast(Optional[Category], cleaned_data.get("category"))
    parent = cast(Optional[Category], cleaned_data.get("parent"))
    parent_id = parent.id if parent else None

    if (
        not errors.has_errors_at_location("parent")
        and parent_id
        and category_obj
        and category_obj.parent_id != parent_id
    ):
        cleaned_data, errors = await validate_data(
            cleaned_data,
            {"parent": [CategoryParentValidator(info.context, category_obj)]},
            errors,
        )

    if errors or not category_obj:
        return {"errors": errors, "category": category_obj}

    updated_category = await update_category(
        category_obj,
        name=cleaned_data["name"],
        is_closed=cleaned_data.get("is_closed") or False,
    )

    if updated_category.parent_id != parent_id:
        categories = await get_all_categories()
        updated_category = await move_category(
            categories, updated_category, parent=parent
        )

    return {"category": updated_category}


class EditCategoryInputModel(CategoryInputModel):  # type: ignore
    category: PositiveInt
