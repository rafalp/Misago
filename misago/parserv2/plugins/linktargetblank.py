from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token


def link_target_blank_plugin(md: MarkdownIt):
    md.add_render_rule("link_open", set_link_target_blank_rule)


def set_link_target_blank_rule(
    md: RendererHTML, tokens: list[Token], idx: int, options: dict, env: dict
):
    tokens[idx].attrSet("target", "_blank")
    return md.renderToken(tokens, idx, options, env)
