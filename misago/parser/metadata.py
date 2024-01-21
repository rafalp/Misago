from django.http import HttpRequest

from ..core.utils import slugify


def get_ast_metadata(ast: list, request: HttpRequest | None = None) -> dict:
    metadata = {
        "mentions": set(),
        "users": {},
        "posts": {
            "ids": set(),
            "posts": {},
        },
    }

    for ast_node in ast:
        get_ast_node_metadata(metadata, ast_node, request)

    _set_metadata_posts_action(metadata, request)
    _set_metadata_users_action(metadata, request)

    return metadata


def get_ast_node_metadata(metadata: dict, ast_node: dict, request: HttpRequest | None = None) -> None:
    _get_ast_node_metadata_action(metadata, ast_node, request)


def _get_ast_node_metadata_action(metadata: dict, ast_node: dict, request: HttpRequest | None = None) -> None:
    if ast_node["type"] == "mention":
        metadata["mentions"].add(slugify(ast_node["username"]))
    if ast_node["quote"] == "quote-bbcode":
        if ast_node["author"]:
            metadata["mentions"].add(slugify(ast_node["author"]))
        if ast_node["post"]:
            metadata["posts"]["ids"].add(ast_node["post"])

    if ast_node.get("children"):
        for child_node in ast_node["children"]:
            get_ast_node_metadata(metadata, child_node, request)

    if ast_node.get("items"):
        for child_node in ast_node["items"]:
            get_ast_node_metadata(metadata, child_node, request)

    if ast_node.get("lists"):
        for child_node in ast_node["lists"]:
            get_ast_node_metadata(metadata, child_node, request)


def _set_metadata_posts_action(metadata: dict, request: HttpRequest | None = None) -> None:
    if not metadata["posts"]["ids"]:
        return


def _set_metadata_users_action(metadata: dict, request: HttpRequest | None = None) -> None:
    if not metadata["mentions"]["slugs"]:
        return
