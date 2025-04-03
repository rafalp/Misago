from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict


def code_plugin(md: MarkdownIt):
    md.add_render_rule("code_block", render_code_rule)


def render_code_rule(
    renderer: RendererHTML,
    tokens: list[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
):
    token = tokens[idx]

    return "<misago-code>" + escapeHtml(token.content.rstrip()) + "</misago-code>\n"
