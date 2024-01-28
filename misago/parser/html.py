from html import escape

from django.utils.translation import pgettext

from ..core.utils import slugify
from .context import ParserContext
from .exceptions import AstError
from .hooks import complete_markup_html_hook, render_ast_node_to_html_hook
from .urls import clean_href

SPOILER_SUMMARY = "<spoiler-summary-message>"


def render_ast_to_html(context: ParserContext, ast: list[dict], metadata: dict) -> str:
    html = ""
    for ast_node in ast:
        node_html = render_ast_node_to_html(context, ast_node, metadata)
        if node_html:
            html += node_html
    return html


def render_ast_node_to_html(
    context: ParserContext, ast_node: dict, metadata: dict
) -> str:
    return render_ast_node_to_html_hook(
        _render_ast_node_to_html_action, context, ast_node, metadata
    )


def _render_ast_node_to_html_action(
    context: ParserContext, ast_node: dict, metadata: dict
) -> str:
    ast_type = ast_node["type"]

    if ast_type in ("heading", "heading-setex"):
        html_tag = f"h{ast_node['level']}"
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<{html_tag}>{children}</{html_tag}>"

    if ast_type == "list":
        html_tag = "ol" if ast_node["ordered"] else "ul"
        children = render_ast_to_html(context, ast_node["items"], metadata)
        return f"<{html_tag}>{children}</{html_tag}>"

    if ast_type == "list-item":
        text = render_ast_to_html(context, ast_node["children"], metadata)
        children = render_ast_to_html(context, ast_node["lists"], metadata)
        return f"<li>{text}{children}</li>"

    if ast_type in ("code", "code-bbcode"):
        if ast_node["syntax"]:
            html_class = f" class=\"language-{ast_node['syntax']}\""
        else:
            html_class = ""
        return f"<pre{html_class}><code>{escape(ast_node['code'])}</code></pre>"

    if ast_type == "code-indented":
        return f"<pre><code>{escape(ast_node['code'])}</code></pre>"

    if ast_type == "code-inline":
        return f"<code>{escape(ast_node['code'])}</code>"

    if ast_type == "quote":
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<blockquote>{children}</blockquote>"

    if ast_type == "quote-bbcode":
        children = render_ast_to_html(context, ast_node["children"], metadata)

        if not ast_node["author"]:
            return f"<blockquote>{children}</blockquote>"

        heading = escape(ast_node["author"])

        return (
            '<aside class="quote-block">'
            f'<div class="quote-heading" data-noquote="1">{heading}</div>'
            f'<blockquote class="quote-body">{children}</blockquote>'
            "</aside>"
        )

    if ast_type == "spoiler-bbcode":
        if ast_node["summary"]:
            summary = escape(ast_node["summary"])
        else:
            summary = SPOILER_SUMMARY
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<details><summary>{summary}</summary>{children}</details>"

    if ast_type == "paragraph":
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<p>{children}</p>"

    if ast_type in ("emphasis", "emphasis-underscore"):
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<em>{children}</em>"

    if ast_type in ("strong", "strong-underscore"):
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<strong>{children}</strong>"

    if ast_type in ("strikethrough", "strikethrough-bbcode"):
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<del>{children}</del>"

    if ast_type == "bold-bbcode":
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<b>{children}</b>"

    if ast_type == "italics-bbcode":
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<i>{children}</i>"

    if ast_type == "underline-bbcode":
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<u>{children}</u>"

    if ast_type == "superscript-bbcode":
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<sup>{children}</sup>"

    if ast_type == "subscript-bbcode":
        children = render_ast_to_html(context, ast_node["children"], metadata)
        return f"<sub>{children}</sub>"

    if ast_type in ("thematic-break", "thematic-break-bbcode"):
        return "<hr />"

    if ast_type in ("image", "image-bbcode"):
        src = escape(clean_href(ast_node["src"]))
        alt = escape(ast_node["alt"]) if ast_node["alt"] else ""
        return f'<img src="{src}" alt="{alt}" />'

    if ast_type in ("url", "url-bbcode"):
        children = render_ast_to_html(context, ast_node["children"], metadata)
        href = escape(clean_href(ast_node["href"]))
        rel = "external nofollow noopener"
        return f'<a href="{href}" rel="{rel}" target="_blank">{children or href}</a>'

    if ast_type in ("auto-link", "auto-url"):
        href = escape(clean_href(ast_node["href"]))
        rel = "external nofollow noopener"
        if ast_node.get("image"):
            return f'<img src="{href}" alt="" />'
        else:
            return f'<a href="{href}" rel="{rel}" target="_blank">{href}</a>'

    if ast_type == "mention":
        username = slugify(ast_node["username"])
        if username not in metadata["users"]:
            return escape("@" + ast_node["username"])

        user = metadata["users"][username]
        return f'<a href="{user.get_absolute_url()}">@{escape(user.username)}</a>'

    if ast_type == "escape":
        return escape(ast_node["character"])

    if ast_type == "line-break":
        return "<br />"

    if ast_type == "text":
        return escape(ast_node["text"])

    raise AstError(f"Unknown AST node type: {ast_type}")


def complete_markup_html(html: str, **kwargs) -> str:
    return complete_markup_html_hook(_complete_markup_html_action, html, **kwargs)


def _complete_markup_html_action(html: str, **kwargs) -> str:
    html = complete_markup_html_spoiler_summary(html)
    return html


def complete_markup_html_spoiler_summary(html: str) -> str:
    if SPOILER_SUMMARY in html:
        html = html.replace(
            SPOILER_SUMMARY, pgettext("spoiler summary", "Reveal spoiler")
        )

    return html
