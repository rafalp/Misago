from markdown_it import MarkdownIt
from markdown_it.token import Token


def set_link_target_blank_rule(
    md: MarkdownIt, tokens: list[Token], idx: int, options: dict, env: dict
):
    tokens[idx].attrSet("target", "_blank")
    return md.renderToken(tokens, idx, options, env)
