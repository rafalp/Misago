from typing import Optional, Type

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt, create_model

from ....categories.errors import CategoryInvalidParentError
from ....categories.get import get_all_categories
from ....categories.loaders import categories_loader
from ....categories.models import Category
from ....categories.tree import move_category
from ....categories.validators import CategoryExistsValidator
from ....validation import ROOT_LOCATION, root_validator, validate_data, validate_model
from ...errorhandler import error_handler
from ..decorators import admin_resolver
from .categoryupdate import validate_parent_value

category_move_mutation = MutationType()


@category_move_mutation.field("categoryMove")
@admin_resolver
@error_handler
@convert_kwargs_to_snake_case
async def resolve_category_move(
    _,
    info: GraphQLResolveInfo,
    *,
    category: str,
    parent: Optional[str] = None,
    before: Optional[str] = None
):
    categories = await get_all_categories()

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
