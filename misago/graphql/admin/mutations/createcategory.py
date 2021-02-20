from ariadne import MutationType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo

from ....categories.create import create_category
from ....categories.update import update_category
from ....categories.get import get_categories_mptt
from ...errorhandler import error_handler
from ..decorators import admin_mutation


create_category_mutation = MutationType()


@create_category_mutation.field("createCategory")
@error_handler
@admin_mutation
@convert_kwargs_to_snake_case
async def resolve_create_category(_, info: GraphQLResolveInfo, *, input: dict):
    categories_tree = await get_categories_mptt()
    categories_map = {c.id: c for c in categories_tree.nodes()}

    name = input["name"]
    parent = input.get("parent")
    is_closed = input.get("is_closed")
    parent_category = None

    if parent:
        parent_id = int(parent)
        if parent_id in categories_map:
            parent_category = categories_map[parent_id]

    new_category = await create_category(
        name=name, parent=parent_category, is_closed=is_closed,
    )
    categories_map[new_category.id] = new_category

    categories_tree.insert_node(new_category, parent_category)
    for category in categories_tree.nodes():
        org_category = categories_map[category.id]
        updated_category = await update_category(
            org_category,
            left=category.left,
            right=category.right,
            depth=category.depth,
        )

        if updated_category.id == new_category.id:
            new_category = updated_category

    return {"category": new_category}
