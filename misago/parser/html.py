from html import escape

from .context import ParserContext


def render_ast_to_html(context: ParserContext, ast: list[dict], metadata: dict) -> str:
    html = ""
    for ast_node in ast:
        node_html = render_ast_node_to_html(context, ast_node, metadata)
        if node_html:
            if html:
                html += "\n"
            html += node_html
    return html


def render_inline_ast_to_html(
    context: ParserContext, ast: list[dict], metadata: dict
) -> str:
    html = ""
    for ast_node in ast:
        html += render_ast_node_to_html(context, ast_node, metadata)
    return html


def render_ast_node_to_html(
    context: ParserContext, ast_node: dict, metadata: dict
) -> str:
    return _render_ast_node_to_html_action(context, ast_node, metadata)


def _render_ast_node_to_html_action(
    context: ParserContext, ast_node: dict, metadata: dict
) -> str:
    ast_type = ast_node["type"]

    if ast_type in ("heading", "heading-setex"):
        html_tag = f"h{ast_node['level']}"
        children = render_inline_ast_to_html(context, ast_node["children"], metadata)
        return f"<{html_tag}>{children}</{html_tag}>"

    if ast_type == "paragraph":
        children = render_inline_ast_to_html(context, ast_node["children"], metadata)
        return f"<p>{children}</p>"

    if ast_type in ("emphasis", "emphasis-underscore"):
        children = render_inline_ast_to_html(context, ast_node["children"], metadata)
        return f"<em>{children}</em>"

    if ast_type in ("strong", "strong-underscore"):
        children = render_inline_ast_to_html(context, ast_node["children"], metadata)
        return f"<strong>{children}</strong>"

    if ast_type == "line-break":
        return "<br />"

    if ast_type in ("thematic-break", "thematic-break-bbcode"):
        return "<hr />"

    if ast_type == "text":
        return escape(ast_node["text"])

    raise ValueError(f"Unknown AST type: {ast_type}")
