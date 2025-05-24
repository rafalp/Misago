from dataclasses import replace

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from markdown_it.token import Token

User = get_user_model()


def replace_mentions_tokens(tokens: list[Token]) -> list[Token]:
    mentions = find_mentioned_users(tokens)
    if not mentions:
        return tokens

    users = get_mentioned_users(mentions)
    new_tokens: list[Token] = []

    for token in tokens:
        if token.type == "inline":
            token = replace_token_inline_mentions(token, users)

        new_tokens.append(token)

    return new_tokens


def find_mentioned_users(tokens: list[Token]) -> list[str]:
    mentions: set[str] = set()

    for token in tokens:
        if token.type == "inline":
            for child_token in token.children:
                if child_token.type == "mention":
                    mentions.add(child_token.meta["slug"])

    return sorted(mentions)[: settings.MISAGO_POST_MENTIONS_LIMIT]


def get_mentioned_users(slugs: list[str]) -> list[dict]:
    queryset = User.objects.values_list("id", "username", "slug").filter(
        is_active=True, slug__in=slugs
    )

    users: dict[str, dict] = {}
    for user_id, user_name, user_slug in queryset:
        users[user_slug] = {
            "id": user_id,
            "username": user_name,
            "url": reverse(
                "misago:user",
                kwargs={"pk": user_id, "slug": user_slug},
            ),
        }

    return users


def replace_token_inline_mentions(token_inline: Token, users: dict[str, dict]) -> Token:
    replaced = False
    new_children: list[Token] = []

    for token in token_inline.children:
        if token.type == "mention":
            replaced = True
            user_data = users.get(token.meta["slug"])

            if user_data:
                new_children += [
                    Token(
                        type="link_open",
                        tag="a",
                        nesting=1,
                        attrs={
                            "href": user_data["url"],
                            "class": "rich-text-mention",
                            "misago-rich-text-mention": user_data["username"],
                        },
                        meta={"mention": user_data["id"]},
                    ),
                    Token(
                        type="text",
                        tag="",
                        nesting=0,
                        content="@" + user_data["username"],
                    ),
                    Token(
                        type="link_close",
                        tag="a",
                        nesting=-1,
                    ),
                ]

            else:
                new_children += [
                    Token(
                        type="mention_not_found_open",
                        tag="span",
                        nesting=1,
                        attrs={
                            "class": "rich-text-mention-not-found",
                            "misago-rich-text-mention": token.meta["slug"],
                        },
                    ),
                    Token(
                        type="text",
                        tag="",
                        nesting=0,
                        content=token.markup,
                    ),
                    Token(
                        type="mention_not_found_close",
                        tag="span",
                        nesting=-1,
                    ),
                ]

        else:
            new_children.append(token)

    if replaced:
        return replace(token_inline, children=new_children)

    return token_inline
