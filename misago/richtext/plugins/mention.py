from mistune import Markdown


MENTION_PATTERN = r"(^|[^\w])@([a-zA-Z0-9]+)"


def parse_mention(parser, m, state: dict):
    if state.get("_in_link"):
        return "text", m.group(0)

    return (
        "mention",
        m.group(2),
        m.group(0),
    )


def render_ast_mention(mention, fallback):
    return {
        "type": "mention",
        "mention": mention,
        "fallback": fallback,
    }


def plugion_mention(markdown: Markdown):
    markdown.inline.register_rule("mention", MENTION_PATTERN, parse_mention)
    markdown.inline.rules.append("mention")

    if markdown.renderer.NAME == "ast":
        markdown.renderer.register("mention", render_ast_mention)
