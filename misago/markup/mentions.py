import re
from typing import Union

from django.contrib.auth import get_user_model

from .htmlparser import (
    ElementNode,
    RootNode,
    TextNode,
)

EXCLUDE_ELEMENTS = ("pre", "code", "a")
USERNAME_RE = re.compile(r"@[0-9a-z]+", re.IGNORECASE)
MENTIONS_LIMIT = 32


def add_mentions(result, root_node):
    if "@" not in result["parsed_text"]:
        return

    mentions = set()
    nodes = []

    find_mentions(root_node, mentions, nodes)

    if not mentions or len(mentions) > MENTIONS_LIMIT:
        return  # No need to run mentions logic

    users_data = get_users_data(mentions)
    if not users_data:
        return  # Mentioned users don't exist

    for node in nodes:
        add_mentions_to_node(node, users_data)

    result["mentions"] = [user[0] for user in users_data.values()]


def find_mentions(
    node: Union[ElementNode, RootNode],
    mentions: set,
    nodes: set,
):
    if isinstance(node, ElementNode) and node.tag in EXCLUDE_ELEMENTS:
        return

    tracked_node = False
    for child in node.children:
        if isinstance(child, TextNode):
            results = find_mentions_in_str(child.text)
            if results:
                mentions.update(results)
                if not tracked_node:
                    tracked_node = True
                    nodes.append(node)
        else:
            find_mentions(child, mentions, nodes)


def find_mentions_in_str(text: str):
    matches = USERNAME_RE.findall(text)
    if not matches:
        return None

    return set([match.lower()[1:] for match in matches])


def get_users_data(mentions):
    User = get_user_model()
    users_data = {}

    queryset = User.objects.filter(slug__in=mentions).values_list(
        "id", "username", "slug"
    )

    for user_id, username, slug in queryset:
        users_data[slug] = (user_id, username)

    return users_data


def add_mentions_to_node(node, users_data):
    new_children = []

    for child in node.children:
        if isinstance(child, TextNode):
            new_children += add_mentions_to_text(child.text, users_data)
        else:
            new_children.append(child)

    node.children = new_children


def add_mentions_to_text(text: str, users_data):
    nodes = []

    while True:
        match = USERNAME_RE.search(text)
        if not match:
            if text:
                nodes.append(TextNode(text=text))
            return nodes

        start, end = match.span()
        user_slug = text[start + 1 : end].lower()

        # Append text between 0 and start to nodes
        if start > 0:
            nodes.append(TextNode(text=text[:start]))

        # Append match string to nodes and keep scanning
        if user_slug not in users_data:
            nodes.append(TextNode(text=text[:end]))
            text = text[end:]
            continue

        user_id, username = users_data[user_slug]
        nodes.append(
            ElementNode(
                tag="a",
                attrs={
                    "href": f"/u/{user_slug}/{user_id}/",
                    "data-quote": f"@{username}",
                },
                children=[TextNode(text=f"@{username}")],
            )
        )

        text = text[end:]
