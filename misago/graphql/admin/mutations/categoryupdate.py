from typing import Optional, Type, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, constr, create_model

from ....categories.get import get_all_categories
from ....categories.models import Category
from ....categories.tree import move_category
from ....categories.validators import validate_category_parent
from ....validation import (
    ROOT_LOCATION,
    CategoryExistsValidator,
    color_validator,
    for_location,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler
from ..decorators import admin_resolver
from .categorycreate import CategoryCreateInputModel

category_update_mutation = MutationType()


@category_update_mutation.field("categoryUpdate")
@admin_resolver
@error_handler
@convert_kwargs_to_snake_case
async def resolve_category_update(
    _,
    info: GraphQLResolveInfo,
    *,
    category: str,
    input: dict,  # pylint: disable=redefined-builtin
):
    input["category"] = category

    cleaned_data, errors = validate_model(CategoryUpdateInputModel, input)
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

    return {"updated": updated_category != category_obj, "category": updated_category}


CategoryUpdateInputModel: Type[BaseModel] = create_model(
    "CategoryUpdateInputModel",
    __base__=CategoryCreateInputModel,
    category=(PositiveInt, ...),
    name=(
        constr(strip_whitespace=True, min_length=1, max_length=255, regex=r"\w"),
        None,
    ),
)


@for_location("parent")
def validate_parent_value(cleaned_data: dict, *_) -> dict:
    if "category" not in cleaned_data:
        return cleaned_data

    if "parent" in cleaned_data:
        validate_category_parent(cleaned_data["category"], cleaned_data["parent"])

    return cleaned_data
