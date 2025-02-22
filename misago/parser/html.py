from html import escape

from ..core.utils import slugify
from .context import ParserContext
from .exceptions import AstError
from .hooks import render_ast_node_to_html_hook
from .htmlelement import html_element
from .urls import clean_displayed_url, clean_url

URL_REL = "external nofollow noopener"
URL_TARGET = "_blank"


def render_ast_to_html(context: ParserContext, ast: list[dict], metadata: dict) -> str:
    html = render_children_ast_to_html(context, ast, metadata)
    return html.replace("\n", "\r\n")


def render_children_ast_to_html(
    context: ParserContext, ast: list[dict], metadata: dict
) -> str:
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
        children = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()
        return f"<{html_tag}>{children}</{html_tag}>"

    if ast_type == "list":
        html_tag = "ol" if ast_node["ordered"] else "ul"
        children = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()
        return f"<{html_tag}>{children}</{html_tag}>"

    if ast_type == "list-item":
        text = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()
        children = render_children_ast_to_html(
            context, ast_node["lists"], metadata
        ).strip()
        return f"<li>{text}{children}</li>"

    if ast_type == "table":
        header = render_children_ast_to_html(context, ast_node["header"], metadata)
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return html_element(
            "table",
            f"<tr>{header}</tr>{children}</table>",
            {"class": "rich-text-table"},
        )

    if ast_type == "table-header":
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return html_element(
            "th",
            render_children_ast_to_html(context, ast_node["children"], metadata),
            {"class": "rich-text-table-cell-align-" + ast_node["align"]},
        )

    if ast_type == "table-row":
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<tr>{children}</tr>"

    if ast_type == "table-cell":
        return html_element(
            "td",
            render_children_ast_to_html(context, ast_node["children"], metadata),
            {"class": "rich-text-table-cell-align-" + ast_node["align"]},
        )

    if ast_type in ("code", "code-bbcode"):
        if ast_node["syntax"]:
            html_class = f"language-{ast_node['syntax']}"
        else:
            html_class = None

        return html_element(
            "pre",
            f"<code>{escape(ast_node['code'])}</code>",
            attrs={"class": html_class},
        )

    if ast_type == "code-indented":
        return f"<pre><code>{escape(ast_node['code'])}</code></pre>"

    if ast_type == "code-inline":
        return f"<code>{escape(ast_node['code'])}</code>"

    if ast_type == "quote":
        children = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()
        return f"<quote>{children}</quote>"

    if ast_type == "quote-bbcode":
        children = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()

        if not ast_node["author"]:
            return f"<quote>{children}</quote>"

        heading = escape(ast_node["author"])

        return (
            "<quote>"
            f"<header>{heading}</header>"
            f"<body>{children}</body>"
            "</quote>"
        )

    if ast_type == "spoiler-bbcode":
        summary = escape(ast_node["summary"] or "")
        children = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()
        return (
            "<spoiler>"
            f"<summary>{summary}</summary>"
            f"<body>{children}</body>"
            "</spoiler>"
        )

    if ast_type == "paragraph":
        children = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()
        return f"<p>{children}</p>"

    if ast_type in ("emphasis", "emphasis-underscore"):
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<em>{children}</em>"

    if ast_type in ("strong", "strong-underscore"):
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<strong>{children}</strong>"

    if ast_type in ("strikethrough", "strikethrough-bbcode"):
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<del>{children}</del>"

    if ast_type == "bold-bbcode":
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<b>{children}</b>"

    if ast_type == "italics-bbcode":
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<i>{children}</i>"

    if ast_type == "underline-bbcode":
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<u>{children}</u>"

    if ast_type == "superscript-bbcode":
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<sup>{children}</sup>"

    if ast_type == "subscript-bbcode":
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        return f"<sub>{children}</sub>"

    if ast_type in ("thematic-break", "thematic-break-bbcode"):
        return "<hr />"

    if ast_type == "attachment-group":
        children = render_children_ast_to_html(
            context, ast_node["children"], metadata
        ).strip()
        return f'<div class="rich-text-attachment-group">{children}</div>'

    if ast_type == "attachment":
        return f"<attachment={ast_node['name']}:{ast_node['slug']}:{ast_node['id']}>"

    if ast_type in ("image", "image-bbcode"):
        return html_element(
            "img",
            attrs={
                "src": clean_url(ast_node["src"]),
                "alt": ast_node["alt"] or "",
                "title": ast_node.get("title"),
            },
        )

    if ast_type in ("url", "url-bbcode"):
        children = render_children_ast_to_html(context, ast_node["children"], metadata)
        href = clean_url(ast_node["href"])
        display_href = clean_displayed_url(href)
        title = ast_node.get("title")

        if title:
            title = f"{title} ({href})"
        elif not children:
            title = None
        elif display_href != clean_displayed_url(children):
            title = href

        return html_element(
            "a",
            children or display_href,
            {
                "href": href,
                "rel": URL_REL,
                "target": URL_TARGET,
                "title": title,
            },
        )

    if ast_type in ("auto-link", "auto-url"):
        href = clean_url(ast_node["href"])
        if ast_node.get("image"):
            return f'<img src="{escape(href)}" alt="" />'
        else:
            display_href = clean_displayed_url(href)
            return html_element(
                "a",
                display_href,
                {
                    "href": href,
                    "rel": URL_REL,
                    "target": URL_TARGET,
                    "title": href if len(href) - len(display_href) > 8 else None,
                },
            )

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
