import pytest

from ..markup import render_tokens_to_markup


def test_render_tokens_to_markup_renders_paragraph(parse_to_tokens):
    tokens = parse_to_tokens("hello")
    assert render_tokens_to_markup(tokens) == "hello"


def test_render_tokens_to_markup_renders_two_paragraphs(parse_to_tokens):
    tokens = parse_to_tokens("hello\n\nworld")
    assert render_tokens_to_markup(tokens) == "hello\n\nworld"


def test_render_tokens_to_markup_renders_header_and_paragraph(parse_to_tokens):
    tokens = parse_to_tokens("# hello\n\nworld")
    assert render_tokens_to_markup(tokens) == "# hello\n\nworld"


def test_render_tokens_to_markup_renders_setex_header_and_paragraph(parse_to_tokens):
    tokens = parse_to_tokens("hello\n=====\n\nworld")
    assert render_tokens_to_markup(tokens) == "hello\n=====\n\nworld"


def test_render_tokens_to_markup_renders_code(parse_to_tokens):
    tokens = parse_to_tokens("wop\n\n    hello\n    world")
    assert render_tokens_to_markup(tokens) == "wop\n\n    hello\n    world"


def test_render_tokens_to_markup_renders_fenced_code(parse_to_tokens):
    tokens = parse_to_tokens("```\nhello")
    assert render_tokens_to_markup(tokens) == "```\nhello\n```"


def test_render_tokens_to_markup_renders_fenced_code_with_info(parse_to_tokens):
    tokens = parse_to_tokens("```info\nhello")
    assert render_tokens_to_markup(tokens) == "```info\nhello\n```"


def test_render_tokens_to_markup_renders_fenced_code_with_syntax(parse_to_tokens):
    tokens = parse_to_tokens("```php\nhello")
    assert render_tokens_to_markup(tokens) == "```php\nhello\n```"


def test_render_tokens_to_markup_renders_fenced_code_with_info_and_syntax(
    parse_to_tokens,
):
    tokens = parse_to_tokens("```info, syntax: php\nhello")
    assert render_tokens_to_markup(tokens) == "```info, syntax: php\nhello\n```"


@pytest.mark.parametrize(
    "markup,result",
    (
        (
            "[code]\nhello\n[/code]",
            "[code]\nhello\n[/code]",
        ),
        (
            "[code=info]\nhello\n[/code]",
            "[code=info]\nhello\n[/code]",
        ),
        (
            '[code="quoted info"]\nhello\n[/code]',
            "[code=quoted info]\nhello\n[/code]",
        ),
        (
            "[code=php]\nhello\n[/code]",
            "[code=php]\nhello\n[/code]",
        ),
        (
            '[code="php"]\nhello\n[/code]',
            "[code=php]\nhello\n[/code]",
        ),
        (
            "[code=info, syntax: php]\nhello\n[/code]",
            "[code=info, syntax: php]\nhello\n[/code]",
        ),
        (
            "[code=info [nested]]\nhello\n[/code]",
            "[code=info \\[nested\\]]\nhello\n[/code]",
        ),
        (
            "[code=info \\[escaped\\]]\nhello\n[/code]",
            "[code=info \\[escaped\\]]\nhello\n[/code]",
        ),
    ),
)
def test_render_tokens_to_markup_renders_code_bbcode(parse_to_tokens, markup, result):
    tokens = parse_to_tokens(markup)
    assert render_tokens_to_markup(tokens) == result


def _test_render_tokens_to_markup_renders_blockquote(parse_to_tokens):
    tokens = parse_to_tokens("> hello")
    assert render_tokens_to_markup(tokens) == "hello"


@pytest.mark.parametrize(
    "markup,result",
    (
        (
            "[quote]\nhello\n[/quote]",
            "[quote]\nhello\n[/quote]",
        ),
        (
            "[quote=info]\nhello\n[/quote]",
            "[quote=info]\nhello\n[/quote]",
        ),
        (
            '[quote="quoted info"]\nhello\n[/quote]',
            "[quote=quoted info]\nhello\n[/quote]",
        ),
        (
            "[quote=John, post: 123]\nhello\n[/quote]",
            "[quote=John, post: 123]\nhello\n[/quote]",
        ),
    ),
)
def test_render_tokens_to_markup_renders_quote_bbcode(parse_to_tokens, markup, result):
    tokens = parse_to_tokens(markup)
    assert render_tokens_to_markup(tokens) == result


def _test_render_tokens_to_markup_renders_quote_bbcode_with_info(parse_to_tokens):
    tokens = parse_to_tokens("[quote=info]hello[/quote]")
    assert render_tokens_to_markup(tokens) == "info:\nhello"


def _test_render_tokens_to_markup_renders_quote_bbcode_with_user(parse_to_tokens):
    tokens = parse_to_tokens("[quote=User, post: 123]hello[/quote]")
    assert render_tokens_to_markup(tokens) == "User, #123:\nhello"


def _test_render_tokens_to_markup_renders_spoiler_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("[spoiler]hello[/spoiler]")
    assert render_tokens_to_markup(tokens) == "hello"


def _test_render_tokens_to_markup_renders_spoiler_bbcode_with_info(parse_to_tokens):
    tokens = parse_to_tokens("[spoiler=info]hello[/spoiler]")
    assert render_tokens_to_markup(tokens) == "info:\nhello"


def _test_render_tokens_to_markup_renders_ordered_list(parse_to_tokens):
    tokens = parse_to_tokens("2. lorem\n3. ipsum")
    assert render_tokens_to_markup(tokens) == "2. lorem\n3. ipsum"


def _test_render_tokens_to_markup_renders_bullet_list(parse_to_tokens):
    tokens = parse_to_tokens("- lorem\n- ipsum")
    assert render_tokens_to_markup(tokens) == "- lorem\n- ipsum"


def _test_render_tokens_to_markup_renders_ordered_list_with_nested_ordered_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("2. lorem\n   1. ipsum\n   2. dolor\n3. met")
    assert render_tokens_to_markup(tokens) == (
        "2. lorem" "\n2. 1. ipsum" "\n2. 2. dolor" "\n3. met"
    )


def _test_render_tokens_to_markup_renders_ordered_list_with_nested_bullet_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("2. lorem\n   - ipsum\n   - dolor\n3. met")
    assert render_tokens_to_markup(tokens) == (
        "2. lorem" "\n2. - ipsum" "\n2. - dolor" "\n3. met"
    )


def _test_render_tokens_to_markup_renders_bullet_list_with_nested_ordered_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("- lorem\n  1. ipsum\n  2. dolor\n- met")
    assert render_tokens_to_markup(tokens) == (
        "- lorem" "\n- 1. ipsum" "\n- 2. dolor" "\n- met"
    )


def _test_render_tokens_to_markup_renders_bullet_list_with_nested_bullet_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("- lorem\n  - ipsum\n  - dolor\n- met")
    assert render_tokens_to_markup(tokens) == (
        "- lorem" "\n- - ipsum" "\n- - dolor" "\n- met"
    )


def _test_render_tokens_to_markup_renders_table(parse_to_tokens):
    tokens = parse_to_tokens(
        "| col1 | col2 | col3|\n| - | - | - |\n| cell1 | cell2 | cell3 |"
    )
    assert render_tokens_to_markup(tokens) == ("col1, col2, col3\ncell1, cell2, cell3")


def _test_render_tokens_to_markup_renders_attachments(parse_to_tokens):
    tokens = parse_to_tokens("<attachment=image.png:1><attachment=video.mp4:2>")
    assert render_tokens_to_markup(tokens) == (
        "<attachment=image.png:1>\n<attachment=video.mp4:2>"
    )


def _test_render_tokens_to_markup_renders_code_inline(parse_to_tokens):
    tokens = parse_to_tokens("Hello, `inline`")
    assert render_tokens_to_markup(tokens) == "Hello, inline"


def _test_render_tokens_to_markup_renders_linkified_link(parse_to_tokens):
    tokens = parse_to_tokens("Hello, https://example.com")
    assert render_tokens_to_markup(tokens) == "Hello, https://example.com"


def _test_render_tokens_to_markup_renders_autolink(parse_to_tokens):
    tokens = parse_to_tokens("Hello, <https://example.com>")
    assert render_tokens_to_markup(tokens) == "Hello, https://example.com"


def _test_render_tokens_to_markup_renders_link(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [Link](https://example.com)")
    assert render_tokens_to_markup(tokens) == "Hello, https://example.com (Link)"


def _test_render_tokens_to_markup_renders_url_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [url]https://example.com[/url]")
    assert render_tokens_to_markup(tokens) == "Hello, https://example.com"


def _test_render_tokens_to_markup_renders_url_bbcode_with_text(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [url=https://example.com]Link[/url]")
    assert render_tokens_to_markup(tokens) == "Hello, https://example.com (Link)"


def _test_render_tokens_to_markup_renders_image(parse_to_tokens):
    tokens = parse_to_tokens("Hello, ![Image](https://example.com/image.png)")
    assert (
        render_tokens_to_markup(tokens)
        == "Hello, https://example.com/image.png (Image)"
    )


def _test_render_tokens_to_markup_renders_image_with_title(parse_to_tokens):
    tokens = parse_to_tokens('Hello, ![Image](https://example.com/image.png "Title")')
    assert (
        render_tokens_to_markup(tokens)
        == "Hello, https://example.com/image.png (Image, Title)"
    )


def _test_render_tokens_to_markup_renders_image_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [img]https://example.com/image.png[/img]")
    assert render_tokens_to_markup(tokens) == "Hello, https://example.com/image.png"


def _test_render_tokens_to_markup_renders_image_bbcode_with_alt(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [img=https://example.com/image.png]Image[/img]")
    assert (
        render_tokens_to_markup(tokens)
        == "Hello, https://example.com/image.png (Image)"
    )


def _test_render_tokens_to_markup_renders_youtube_video(parse_to_tokens):
    tokens = parse_to_tokens("https://www.youtube.com/watch?v=QzfXag4r7Vo")
    assert (
        render_tokens_to_markup(tokens) == "https://www.youtube.com/watch?v=QzfXag4r7Vo"
    )


def _test_render_tokens_to_markup_renders_mention(parse_to_tokens, user):
    tokens = parse_to_tokens(f"Hello, @{user.username}")
    assert render_tokens_to_markup(tokens) == f"Hello, @{user.username}"


def _test_render_tokens_to_markup_renders_soft_linebreak(parse_to_tokens):
    tokens = parse_to_tokens("hello\nworld")
    assert render_tokens_to_markup(tokens) == "hello\nworld"
