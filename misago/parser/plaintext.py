import re

from ..core.utils import slugify
from .context import ParserContext
from .enums import PlainTextFormat
from .exceptions import AstError
from .hooks import render_ast_node_to_plaintext_hook
from .urls import clean_url


def render_ast_to_plaintext(
    context: ParserContext,
    ast: list[dict],
    metadata: dict,
    text_format: str | None = None,
) -> str:
    text = render_children_ast_to_plaintext(context, ast, metadata, text_format)

    if text_format in (
        PlainTextFormat.META_DESCRIPTION,
        PlainTextFormat.SEARCH_DOCUMENT,
    ):
        return re.sub("\s\s+", " ", text)

    return text.replace("\n", "\r\n")


def render_children_ast_to_plaintext(
    context: ParserContext,
    ast: list[dict],
    metadata: dict,
    text_format: str | None = None,
) -> str:
    plain_text = []
    for ast_node in ast:
        node_text = render_ast_node_to_plaintext(
            context,
            ast_node,
            metadata,
            text_format,
        ).strip()
        if node_text:
            plain_text.append(node_text)

    return (" ".join(plain_text)).strip()


def render_inline_ast_to_plaintext(
    context: ParserContext,
    ast: list[dict],
    metadata: dict,
    text_format: str | None = None,
) -> str:
    plain_text = ""
    for ast_node in ast:
        plain_text += render_ast_node_to_plaintext(
            context,
            ast_node,
            metadata,
            text_format,
        )
    return plain_text


def render_ast_node_to_plaintext(
    context: ParserContext,
    ast_node: dict,
    metadata: dict,
    text_format: str | None,
) -> str:
    return render_ast_node_to_plaintext_hook(
        _render_ast_node_to_plaintext_action,
        context,
        ast_node,
        metadata,
        text_format,
    )


AST_INLINE_NODES = (
    "heading",
    "heading-setex",
    "paragraph",
    "emphasis",
    "emphasis-underscore",
    "strong",
    "strong-underscore",
    "strikethrough",
    "strikethrough-bbcode",
    "bold-bbcode",
    "italics-bbcode",
    "underline-bbcode",
    "superscript-bbcode",
    "subscript-bbcode",
)


def _render_ast_node_to_plaintext_action(
    context: ParserContext,
    ast_node: dict,
    metadata: dict,
    text_format: str | None,
) -> str:
    ast_type = ast_node["type"]

    if ast_type in AST_INLINE_NODES:
        return render_inline_ast_to_plaintext(
            context, ast_node["children"], metadata, text_format
        ).strip()

    if ast_type == "list":
        items: list[str] = []
        for i, ast_item in enumerate(ast_node["children"]):
            if children := render_inline_ast_to_plaintext(
                context, ast_item["children"], metadata, text_format
            ).strip():
                item = ""
                if ast_node["ordered"]:
                    item += f"{i + 1}."
                else:
                    item += ast_node["sign"]

                item += " " + children
                if lists := render_children_ast_to_plaintext(
                    context, ast_item["lists"], metadata, text_format
                ):
                    item += " " + lists

                items.append(item)

        return " ".join(items)

    if ast_type == "table":
        items: list[str] = []
        for header in ast_node["header"]:
            if header["children"]:
                items.append(
                    render_inline_ast_to_plaintext(
                        context, header["children"], metadata, text_format
                    ).strip()
                )
        for row in ast_node["children"]:
            for cell in row["children"]:
                if cell["children"]:
                    items.append(
                        render_inline_ast_to_plaintext(
                            context, cell["children"], metadata, text_format
                        ).strip()
                    )

        return " ".join(items)

    if ast_type in ("code", "code-bbcode", "code-indented"):
        code_lines = [
            line.strip() for line in ast_node["code"].splitlines() if line.strip()
        ]
        if syntax := ast_node["syntax"]:
            return f"{syntax}: " + " ".join(code_lines)
        return " ".join(code_lines)

    if ast_type == "code-inline":
        return ast_node["code"]

    if ast_type in ("quote", "quote-bbcode"):
        children = render_children_ast_to_plaintext(
            context, ast_node["children"], metadata, text_format
        )

        if author := ast_node.get("author"):
            return f"{author}: {children}"

        return children

    if ast_type == "spoiler-bbcode":
        children = render_children_ast_to_plaintext(
            context, ast_node["children"], metadata, text_format
        )

        if summary := ast_node["summary"]:
            return f"{summary}: {children}"

        return children

    if ast_type in ("image", "image-bbcode"):
        alt = ast_node["alt"] or ""
        title = ast_node.get("title") or ""

        if title == alt:
            title = ""

        if text_format == PlainTextFormat.META_DESCRIPTION:
            return f"{alt} {title}".strip()

        src = clean_url(ast_node["src"])
        return " ".join(i for i in (alt, src, title) if i).strip()

    if ast_type in ("url", "url-bbcode"):
        href = clean_url(ast_node["href"])
        title = ast_node.get("title") or ""

        if children := render_inline_ast_to_plaintext(
            context, ast_node["children"], metadata, text_format
        ).strip():
            if text_format == PlainTextFormat.META_DESCRIPTION:
                if title:
                    return f"{children} ({title})"
                return children
            else:
                if title:
                    return f"{children} ({title}) {href}"
                return f"{children} {href}"

        if text_format == PlainTextFormat.META_DESCRIPTION:
            return title

        return f"{title} {href}".strip()

    if ast_type == "attachment-group":
        return render_children_ast_to_plaintext(
            context, ast_node["children"], metadata, text_format
        )

    if ast_type == "attachment":
        return ast_node["name"]

    if ast_type in ("auto-link", "auto-url"):
        if text_format == PlainTextFormat.META_DESCRIPTION:
            return ""

        return clean_url(ast_node["href"])

    if ast_type == "mention":
        username = slugify(ast_node["username"])
        if username not in metadata["users"]:
            return "@" + ast_node["username"]

        user = metadata["users"][username]
        return "@" + user.username

    if ast_type == "escape":
        return ast_node["character"]

    if ast_type in ("thematic-break", "thematic-break-bbcode", "line-break"):
        return " "

    if ast_type == "text":
        return ast_node["text"]

    raise AstError(f"Unknown AST node type: {ast_type}")
