from django.shortcuts import render
from django.utils.translation import pgettext_lazy

from .context import ParserContext, create_parser_context
from .enums import ContentType, PlainTextFormat
from .factory import create_parser
from .html import render_ast_to_html
from .metadata import create_ast_metadata


def formatting_help(request):
    context = create_parser_context(request)
    parser = create_parser(context)

    examples = []
    for name, markup in FORMATS:
        markup = str(markup)
        if "@username" in markup and request.user.is_authenticated:
            markup = markup.replace("@username", "@" + request.user.username)

        ast = parser(markup)
        metadata = create_ast_metadata(context, ast)

        examples.append(
            {
                "name": str(name),
                "markup": markup,
                "html": render_ast_to_html(context, ast, metadata),
            }
        )

    if request.is_htmx:
        template_name = "misago/formatting_help/modal.html"
    else:
        template_name = "misago/formatting_help/page.html"

    return render(request, template_name, {"examples": examples})


FORMATS = [
    (
        pgettext_lazy("formatting help", "Emphasis text"),
        pgettext_lazy("formatting help", "_This text will have emphasis_"),
    ),
    (
        pgettext_lazy("formatting help", "Bold text"),
        pgettext_lazy("formatting help", "**This text will be bold**"),
    ),
    (
        pgettext_lazy("formatting help", "Removed text"),
        pgettext_lazy("formatting help", "~~This text will be removed~~"),
    ),
    (
        pgettext_lazy("formatting help", "Bold text (BBCode)"),
        pgettext_lazy("formatting help", "[b]This text will be bold[/b]"),
    ),
    (
        pgettext_lazy("formatting help", "Underlined text (BBCode)"),
        pgettext_lazy("formatting help", "[u]This text will be underlined[/u]"),
    ),
    (
        pgettext_lazy("formatting help", "Italics text (BBCode)"),
        pgettext_lazy("formatting help", "[i]This text will be in italics[/i]"),
    ),
    (
        pgettext_lazy("formatting help", "Link"),
        pgettext_lazy("formatting help", "<http://example.com>"),
    ),
    (
        pgettext_lazy("formatting help", "Link with text"),
        pgettext_lazy("formatting help", "[Link text](http://example.com)"),
    ),
    (
        pgettext_lazy("formatting help", "Link (BBCode)"),
        pgettext_lazy("formatting help", "[url]http://example.com[/url]"),
    ),
    (
        pgettext_lazy("formatting help", "Link with text (BBCode)"),
        pgettext_lazy("formatting help", "[url=http://example.com]Link text[/url]"),
    ),
    (
        pgettext_lazy("formatting help", "Image"),
        pgettext_lazy("formatting help", "!(https://dummyimage.com/38x38/000/fff.png)"),
    ),
    (
        pgettext_lazy("formatting help", "Image with alternate text"),
        pgettext_lazy(
            "formatting help", "![Image text](https://dummyimage.com/38x38/000/fff.png)"
        ),
    ),
    (
        pgettext_lazy("formatting help", "Image (BBCode)"),
        pgettext_lazy(
            "formatting help", "[img]https://dummyimage.com/38x38/000/fff.png[/img]"
        ),
    ),
    (
        pgettext_lazy("formatting help", "Mention user by their name"),
        pgettext_lazy("formatting help", "@username"),
    ),
    (
        pgettext_lazy("formatting help", "Heading 1"),
        pgettext_lazy("formatting help", "# First level heading"),
    ),
    (
        pgettext_lazy("formatting help", "Heading 2"),
        pgettext_lazy("formatting help", "## Second level heading"),
    ),
    (
        pgettext_lazy("formatting help", "Heading 3"),
        pgettext_lazy("formatting help", "### Third level heading"),
    ),
    (
        pgettext_lazy("formatting help", "Heading 4"),
        pgettext_lazy("formatting help", "#### Fourth level heading"),
    ),
    (
        pgettext_lazy("formatting help", "Heading 5"),
        pgettext_lazy("formatting help", "##### Fifth level heading"),
    ),
    (
        pgettext_lazy("formatting help", "Unordered list"),
        pgettext_lazy(
            "formatting help", "- Lorem ipsum\r\n- Dolor met\r\n- Vulputate lectus"
        ),
    ),
    (
        pgettext_lazy("formatting help", "Ordered list"),
        pgettext_lazy(
            "formatting help", "1. Lorem ipsum\r\n2. Dolor met\r\n3. Vulputate lectus"
        ),
    ),
    (
        pgettext_lazy("formatting help", "Table"),
        pgettext_lazy(
            "formatting help",
            "| Left aligned | Center aligned | Right aligned |\r\n| ------------ | :------------: | ------------: |\r\n| Cell 1       | Cell 2         | Cell 3        |\r\n| Cell 4       | Cell 5         | Cell 6        |",
        ),
    ),
    (
        pgettext_lazy("formatting help", "Quote text"),
        pgettext_lazy("formatting help", "> Quoted text"),
    ),
    (
        pgettext_lazy("formatting help", "Quote text (BBCode)"),
        pgettext_lazy("formatting help", "[quote]\r\nQuoted text\r\n[/quote]"),
    ),
    (
        pgettext_lazy("formatting help", "Quote text with author (BBCode)"),
        pgettext_lazy(
            "formatting help", '[quote="Quote author"]\r\nQuoted text\r\n[/quote]'
        ),
    ),
    (
        pgettext_lazy("formatting help", "Spoiler"),
        pgettext_lazy("formatting help", "[spoiler]\r\nSecret text\r\n[/spoiler]"),
    ),
    (
        pgettext_lazy("formatting help", "Inline code"),
        pgettext_lazy("formatting help", "`inline code`"),
    ),
    (
        pgettext_lazy("formatting help", "Code block"),
        pgettext_lazy("formatting help", '```\r\nalert("Hello world!");\r\n```'),
    ),
    (
        pgettext_lazy("formatting help", "Code block with syntax highlighting"),
        pgettext_lazy("formatting help", '```python\r\nalert("Hello world!");\r\n```'),
    ),
    (
        pgettext_lazy("formatting help", "Code block (BBCode)"),
        pgettext_lazy("formatting help", '[code]\r\nalert("Hello world!");\r\n[/code]'),
    ),
    (
        pgettext_lazy(
            "formatting help", "Code block with syntax highlighting (BBCode)"
        ),
        pgettext_lazy(
            "formatting help", '[code=python]\r\nprint("Hello world!");\r\n[/code]'
        ),
    ),
    (
        pgettext_lazy("formatting help", "Horizontal rule"),
        pgettext_lazy("formatting help", "Lorem ipsum\r\n- - -\r\nDolor met"),
    ),
    (
        pgettext_lazy("formatting help", "Horizontal rule (BBCode)"),
        pgettext_lazy("formatting help", "Lorem ipsum\r\n[hr]\r\nDolor met"),
    ),
]
