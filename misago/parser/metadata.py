from typing import Iterable

from django.conf import settings
from django.contrib.auth import get_user_model

from ..core.utils import slugify
from .context import ParserContext
from .hooks import (
    get_ast_metadata_users_queryset_hook,
    update_ast_metadata_hook,
    update_ast_metadata_from_node_hook,
    update_ast_metadata_users_hook,
)

User = get_user_model()


def create_ast_metadata(
    context: ParserContext,
    ast: list[dict],
) -> dict:
    metadata = {
        "mentions": set(),
        "users": {},
        "posts": {
            "ids": set(),
            "objs": {},
        },
    }

    return update_ast_metadata_hook(_update_ast_metadata_action, context, ast, metadata)


def _update_ast_metadata_action(
    context: ParserContext,
    ast: list[dict],
    metadata: dict,
) -> dict:
    for ast_node in ast:
        update_ast_metadata_from_node(context, ast_node, metadata)

    update_ast_metadata_users_hook(_update_ast_metadata_users_action, context, metadata)

    return metadata


def update_ast_metadata_from_node(
    context: ParserContext,
    ast_node: dict,
    metadata: dict,
) -> None:
    update_ast_metadata_from_node_hook(
        _update_ast_metadata_from_node_action, context, ast_node, metadata
    )


def _update_ast_metadata_from_node_action(
    context: ParserContext,
    ast_node: dict,
    metadata: dict,
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


def _update_ast_metadata_users_action(context: ParserContext, metadata: dict) -> None:
    if not metadata["mentions"]:
        return

    mentions = sorted(metadata["mentions"])
    if len(mentions) > settings.MISAGO_PARSER_MAX_MENTIONS:
        return

    if mentions:
        queryset = get_ast_metadata_users_queryset(context, mentions)
        for user in queryset:
            metadata["users"][user.slug] = user


def get_ast_metadata_users_queryset(
    context: ParserContext, mentions: list[str]
) -> Iterable[User]:
    return get_ast_metadata_users_queryset_hook(
        _get_ast_metadata_users_queryset_action, context, mentions
    )


def _get_ast_metadata_users_queryset_action(
    context: ParserContext,
    mentions: list[str],
) -> Iterable[User]:
    return User.objects.filter(slug__in=mentions)
