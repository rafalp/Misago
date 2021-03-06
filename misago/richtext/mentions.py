from typing import List

from ..types import ParsedMarkupMetadata
from ..users.get import get_users_by_name

MAX_MENTIONED_USERS = 20


def find_user_mentions(ast: List[dict], metadata: ParsedMarkupMetadata):
    for node in ast:
        if node["type"] == "quote_bbcode" and node["author"]:
            mention = clean_mention(node["author"])
            if mention not in metadata["mentions"]:
                metadata["mentions"].append(mention)

        if node["type"] == "mention" and node["mention"]:
            mention = clean_mention(node["mention"])
            if mention not in metadata["mentions"]:
                metadata["mentions"].append(mention)

        if "children" in node and isinstance(node["children"], list):
            find_user_mentions(node["children"], metadata)


def clean_mention(mention: str) -> str:
    mention = mention.lower()
    if mention.startswith("@"):
        mention = mention.lstrip("@")
    return mention


async def update_metadata_from_mentions(metadata: dict):
    if not metadata["mentions"]:
        return

    users = await get_users_by_name(metadata["mentions"][:MAX_MENTIONED_USERS])

    for user in users:
        metadata["users"][user.slug] = user
