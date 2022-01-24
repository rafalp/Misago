from typing import Optional, cast

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, PositiveInt

from ....categories.contents import delete_categories_contents, move_categories_contents
from ....categories.errors import CategoryInvalidError
from ....categories.get import get_all_categories
from ....categories.models import Category
from ....categories.tree import delete_category, move_category
from ....errors import ErrorsList
from ....loaders import clear_categories
from ....validation import (
    ROOT_LOCATION,
    CategoryExistsValidator,
    for_location,
    validate_data,
    validate_model,
)
from ...errorhandler import error_handler
from ..decorators import admin_resolver

category_delete_mutation = MutationType()


@category_delete_mutation.field("categoryDelete")
@admin_resolver
@error_handler
@convert_kwargs_to_snake_case
async def resolve_category_delete(
    _,
    info: GraphQLResolveInfo,
    *,
    category: str,
    move_threads_to: Optional[str] = None,
    move_children_to: Optional[str] = None,
):
    categories = await get_all_categories()

    input_data = {
        "category": category,
        "move_threads_to": move_threads_to,
        "move_children_to": move_children_to,
    }

    cleaned_data, errors = validate_model(DeleteCategoryInputModel, input_data)
    cleaned_data, errors = await validate_data(
        cleaned_data,
        {
            "category": [CategoryExistsValidator(info.context)],
            "move_threads_to": [CategoryExistsValidator(info.context)],
            "move_children_to": [CategoryExistsValidator(info.context)],
            ROOT_LOCATION: [
                validate_move_threads_to_value,
                validate_move_children_to_value,
            ],
        },
        errors,
    )

    category_obj = cast(Optional[Category], cleaned_data.get("category"))
    if errors or not category_obj:
        root_categories = [c for c in categories if c.depth == 0]
        return {"errors": errors, "deleted": False, "categories": root_categories}

    if cleaned_data["move_children_to"]:
        for child in categories:
            if child.parent_id == category_obj.id:
                _, categories = await move_category(
                    categories, child, parent=cleaned_data["move_children_to"]
                )

    categories_removed = [category_obj]
    if not cleaned_data["move_children_to"]:
        for child in categories:
            if child.is_child(category_obj):
                categories_removed.append(child)

    if not cleaned_data["move_threads_to"]:
        await delete_categories_contents(categories_removed)
    else:
        await move_categories_contents(
            categories_removed, cleaned_data["move_threads_to"]
        )

    categories = await delete_category(categories, category_obj)

    clear_categories(info.context)

    root_categories = [c for c in categories if c.depth == 0]
    return {"deleted": True, "categories": root_categories}


class DeleteCategoryInputModel(BaseModel):  # type: ignore
    category: PositiveInt
    move_threads_to: Optional[PositiveInt]
    move_children_to: Optional[PositiveInt]


@for_location("move_threads_to")
def validate_move_threads_to_value(cleaned_data: dict, errors: ErrorsList, *_) -> dict:
    if errors:
        return cleaned_data

    category = cleaned_data["category"]
    move_threads_to = cleaned_data["move_threads_to"]
    move_children_to = cleaned_data["move_children_to"]

    if move_threads_to:
        if category.id == move_threads_to.id:
            raise CategoryInvalidError(category_id=move_threads_to.id)
        if not move_children_to and move_threads_to.is_child(category):
            raise CategoryInvalidError(category_id=move_threads_to.id)

    return cleaned_data


@for_location("move_children_to")
def validate_move_children_to_value(cleaned_data: dict, errors: ErrorsList, *_) -> dict:
    if errors:
        return cleaned_data

    category = cleaned_data["category"]
    move_children_to = cleaned_data["move_children_to"]

    if move_children_to and (
        category.id == move_children_to.id
        or move_children_to.is_child(category)
        or move_children_to.depth
    ):
        raise CategoryInvalidError(category_id=move_children_to.id)

    return cleaned_data
