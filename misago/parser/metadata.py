from django.contrib.auth.models import get_user_model

from ..core.utils import slugify
from .context import ParserContext
from .hooks import (
    create_ast_metadata_hook,
    update_ast_metadata_from_node_hook,
    update_ast_metadata_posts_hook,
    update_ast_metadata_users_hook,
)

User = get_user_model()


def create_ast_metadata(
    ast: list[dict],
    context: ParserContext,
) -> dict:
    metadata = {
        "mentions": set(),
        "users": {},
        "posts": {
            "ids": set(),
            "objs": {},
        },
    }

    return create_ast_metadata_hook(_create_ast_metadata_action, metadata, ast, context)


def _create_ast_metadata_action(
    metadata: dict,
    ast: list[dict],
    context: ParserContext,
) -> dict:
    for ast_node in ast:
        update_ast_metadata_from_node(metadata, ast_node, context)

    update_ast_metadata_posts_hook(_update_ast_metadata_posts_action, metadata, context)

    update_ast_metadata_users_hook(_update_ast_metadata_users_action, metadata, context)

    return metadata


def update_ast_metadata_from_node(
    metadata: dict,
    ast_node: dict,
    context: ParserContext,
) -> None:
    update_ast_metadata_from_node_hook(
        _update_ast_metadata_from_node_action, metadata, ast_node, context
    )


def _update_ast_metadata_from_node_action(
    metadata: dict,
    ast_node: dict,
    context: ParserContext,
) -> None:
    if ast_node["type"] == "mention":
        metadata["mentions"].add(slugify(ast_node["username"]))

    elif ast_node["type"] == "quote-bbcode":
        if ast_node["author"]:
            metadata["mentions"].add(slugify(ast_node["author"]))
        if ast_node["post"]:
            metadata["posts"]["ids"].add(ast_node["post"])

    if ast_node.get("children"):
        for child_node in ast_node["children"]:
            update_ast_metadata_from_node(metadata, child_node, context)

    if ast_node.get("items"):
        for child_node in ast_node["items"]:
            update_ast_metadata_from_node(metadata, child_node, context)

    if ast_node.get("lists"):
        for child_node in ast_node["lists"]:
            update_ast_metadata_from_node(metadata, child_node, context)


def _update_ast_metadata_posts_action(metadata: dict, context: ParserContext) -> None:
    if not metadata["posts"]["ids"]:
        return

    return  # TODO when posts perms are done!


def _update_ast_metadata_users_action(metadata: dict, context: ParserContext) -> None:
    if not metadata["mentions"]["slugs"]:
        return
