from markdown_it import MarkdownIt
from markdown_it.token import Token


def url_target_blank_plugin(md: MarkdownIt):
    md.add_render_rule("link_open", set_url_target_blank_rule)


def set_url_target_blank_rule(
    md: MarkdownIt, tokens: list[Token], idx: int, options: dict, env: dict
):
    tokens[idx].attrSet("target", "_blank")
    return md.renderToken(tokens, idx, options, env)
