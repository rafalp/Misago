from typing import Optional

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, create_model

from ....categories.get import get_all_categories
from ....categories.update import update_category
from ....validation import (
    CategoryExistsValidator,
    CategoryMaxDepthValidator,
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
    # categories = await get_all_categories()

    input["category"] = category

    cleaned_data, errors = validate_model(EditCategoryInputModel, input)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {
            "category": [CategoryExistsValidator(info.context),],
            "parent": [
                CategoryExistsValidator(info.context),
                CategoryMaxDepthValidator(info.context, max_depth=0),
            ],
        },
        errors,
    )

    category = cleaned_data.get("category")
    parent = cleaned_data.get("parent")
    parent_id = parent.id if parent else None

    if not errors.has_errors_at_location("parent") and category.parent_id != parent_id:
        pass  # todo: run extra validation for new parent

    if errors:
        return {"errors": errors, "category": category}

    updated_category = await update_category(
        category,
        name=cleaned_data["name"],
        is_closed=cleaned_data.get("is_closed") or False,
    )

    if updated_category.parent_id != parent_id:
        pass

    return {"category": updated_category}


class EditCategoryInputModel(CategoryInputModel):
    category: PositiveInt
