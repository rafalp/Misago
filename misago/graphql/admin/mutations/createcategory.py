from typing import Optional

from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ....categories.create import create_category
from ....categories.get import get_all_categories
from ....categories.tree import insert_category
from ....validation import (
    CategoryExistsValidator,
    CategoryMaxDepthValidator,
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
        {
            "parent": [
                CategoryExistsValidator(info.context),
                CategoryMaxDepthValidator(info.context, max_depth=0),
            ]
        },
        errors,
    )

    if errors:
        return {"errors": errors}

    new_category = await create_category(
        name=cleaned_data["name"],
        parent=cleaned_data.get("parent"),
        is_closed=cleaned_data.get("is_closed") or False,
    )
    new_category = await insert_category(
        categories, new_category, cleaned_data.get("parent")
    )

    return {"category": new_category}


CategoryInputModel = create_model(
    "CategoryInputModel",
    name=(
        constr(strip_whitespace=True, min_length=1, max_length=255, regex=r"\w"),
        ...,
    ),
    parent=(Optional[PositiveInt], ...),
    is_closed=(Optional[bool], False),
)
