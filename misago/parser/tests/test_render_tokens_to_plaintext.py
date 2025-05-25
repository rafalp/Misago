from ..plaintext import render_tokens_to_plaintext


def test_render_tokens_to_plaintext_renders_paragraph(parse_to_tokens):
    tokens = parse_to_tokens("hello")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_two_paragraphs(parse_to_tokens):
    tokens = parse_to_tokens("hello\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


def test_render_tokens_to_plaintext_renders_header_and_paragraph(parse_to_tokens):
    tokens = parse_to_tokens("# hello\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


def test_render_tokens_to_plaintext_renders_setex_header_and_paragraph(parse_to_tokens):
    tokens = parse_to_tokens("hello\n=====\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


def test_render_tokens_to_plaintext_renders_code(parse_to_tokens):
    tokens = parse_to_tokens("    hello\n    world")
    assert render_tokens_to_plaintext(tokens) == "hello\nworld"


def test_render_tokens_to_plaintext_renders_fenced_code(parse_to_tokens):
    tokens = parse_to_tokens("```\nhello")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_info(parse_to_tokens):
    tokens = parse_to_tokens("```info\nhello")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_syntax(parse_to_tokens):
    tokens = parse_to_tokens("```php\nhello")
    assert render_tokens_to_plaintext(tokens) == "php:\nhello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_info_and_syntax(
    parse_to_tokens,
):
    tokens = parse_to_tokens("```info, syntax: php\nhello")
    assert render_tokens_to_plaintext(tokens) == "info, php:\nhello"


def test_render_tokens_to_plaintext_renders_code_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("[code]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_code_bbcode_with_info(parse_to_tokens):
    tokens = parse_to_tokens("[code=info]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_code_bbcode_with_syntax(parse_to_tokens):
    tokens = parse_to_tokens("[code=php]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "php:\nhello"


def test_render_tokens_to_plaintext_renders_code_bbcode_with_info_and_syntax(
    parse_to_tokens,
):
    tokens = parse_to_tokens("[code=info, syntax: php]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "info, php:\nhello"


def test_render_tokens_to_plaintext_renders_blockquote(parse_to_tokens):
    tokens = parse_to_tokens("> hello")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_quote_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("[quote]hello[/quote]")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_quote_bbcode_with_info(parse_to_tokens):
    tokens = parse_to_tokens("[quote=info]hello[/quote]")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_quote_bbcode_with_user(parse_to_tokens):
    tokens = parse_to_tokens("[quote=User, post: 123]hello[/quote]")
    assert render_tokens_to_plaintext(tokens) == "User, #123:\nhello"


def test_render_tokens_to_plaintext_renders_spoiler_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("[spoiler]hello[/spoiler]")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_spoiler_bbcode_with_info(parse_to_tokens):
    tokens = parse_to_tokens("[spoiler=info]hello[/spoiler]")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_ordered_list(parse_to_tokens):
    tokens = parse_to_tokens("2. lorem\n3. ipsum")
    assert render_tokens_to_plaintext(tokens) == "2. lorem\n3. ipsum"


def test_render_tokens_to_plaintext_renders_bullet_list(parse_to_tokens):
    tokens = parse_to_tokens("- lorem\n- ipsum")
    assert render_tokens_to_plaintext(tokens) == "- lorem\n- ipsum"


def test_render_tokens_to_plaintext_renders_ordered_list_with_nested_ordered_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("2. lorem\n   1. ipsum\n   2. dolor\n3. met")
    assert render_tokens_to_plaintext(tokens) == (
        "2. lorem" "\n2. 1. ipsum" "\n2. 2. dolor" "\n3. met"
    )


def test_render_tokens_to_plaintext_renders_ordered_list_with_nested_bullet_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("2. lorem\n   - ipsum\n   - dolor\n3. met")
    assert render_tokens_to_plaintext(tokens) == (
        "2. lorem" "\n2. - ipsum" "\n2. - dolor" "\n3. met"
    )


def test_render_tokens_to_plaintext_renders_bullet_list_with_nested_ordered_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("- lorem\n  1. ipsum\n  2. dolor\n- met")
    assert render_tokens_to_plaintext(tokens) == (
        "- lorem" "\n- 1. ipsum" "\n- 2. dolor" "\n- met"
    )


def test_render_tokens_to_plaintext_renders_bullet_list_with_nested_bullet_list(
    parse_to_tokens,
):
    tokens = parse_to_tokens("- lorem\n  - ipsum\n  - dolor\n- met")
    assert render_tokens_to_plaintext(tokens) == (
        "- lorem" "\n- - ipsum" "\n- - dolor" "\n- met"
    )


def test_render_tokens_to_plaintext_renders_table(parse_to_tokens):
    tokens = parse_to_tokens(
        "| col1 | col2 | col3|\n| - | - | - |\n| cell1 | cell2 | cell3 |"
    )
    assert render_tokens_to_plaintext(tokens) == (
        "col1, col2, col3\ncell1, cell2, cell3"
    )


def test_render_tokens_to_plaintext_renders_attachments(parse_to_tokens):
    tokens = parse_to_tokens("<attachment=image.png:1><attachment=video.mp4:2>")
    assert render_tokens_to_plaintext(tokens) == "image.png\n\nvideo.mp4"


def test_render_tokens_to_plaintext_renders_code_inline(parse_to_tokens):
    tokens = parse_to_tokens("Hello, `inline`")
    assert render_tokens_to_plaintext(tokens) == "Hello, inline"


def test_render_tokens_to_plaintext_renders_linkified_link(parse_to_tokens):
    tokens = parse_to_tokens("Hello, https://example.com")
    assert render_tokens_to_plaintext(tokens) == "Hello, https://example.com"


def test_render_tokens_to_plaintext_renders_autolink(parse_to_tokens):
    tokens = parse_to_tokens("Hello, <https://example.com>")
    assert render_tokens_to_plaintext(tokens) == "Hello, https://example.com"


def test_render_tokens_to_plaintext_renders_link(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [Link](https://example.com)")
    assert render_tokens_to_plaintext(tokens) == "Hello, https://example.com (Link)"


def test_render_tokens_to_plaintext_renders_url_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [url]https://example.com[/url]")
    assert render_tokens_to_plaintext(tokens) == "Hello, https://example.com"


def test_render_tokens_to_plaintext_renders_url_bbcode_with_text(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [url=https://example.com]Link[/url]")
    assert render_tokens_to_plaintext(tokens) == "Hello, https://example.com (Link)"


def test_render_tokens_to_plaintext_renders_image(parse_to_tokens):
    tokens = parse_to_tokens("Hello, ![Image](https://example.com/image.png)")
    assert (
        render_tokens_to_plaintext(tokens)
        == "Hello, https://example.com/image.png (Image)"
    )


def test_render_tokens_to_plaintext_renders_image_with_title(parse_to_tokens):
    tokens = parse_to_tokens('Hello, ![Image](https://example.com/image.png "Title")')
    assert (
        render_tokens_to_plaintext(tokens)
        == "Hello, https://example.com/image.png (Image, Title)"
    )


def test_render_tokens_to_plaintext_renders_image_bbcode(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [img]https://example.com/image.png[/img]")
    assert render_tokens_to_plaintext(tokens) == "Hello, https://example.com/image.png"


def test_render_tokens_to_plaintext_renders_image_bbcode_with_alt(parse_to_tokens):
    tokens = parse_to_tokens("Hello, [img=https://example.com/image.png]Image[/img]")
    assert (
        render_tokens_to_plaintext(tokens)
        == "Hello, https://example.com/image.png (Image)"
    )


def test_render_tokens_to_plaintext_renders_youtube_video(parse_to_tokens):
    tokens = parse_to_tokens("https://www.youtube.com/watch?v=QzfXag4r7Vo")
    assert (
        render_tokens_to_plaintext(tokens)
        == "https://www.youtube.com/watch?v=QzfXag4r7Vo"
    )


def test_render_tokens_to_plaintext_renders_mention(parse_to_tokens, user):
    tokens = parse_to_tokens(f"Hello, @{user.username}")
    assert render_tokens_to_plaintext(tokens) == f"Hello, @{user.username}"


def test_render_tokens_to_plaintext_renders_soft_linebreak(parse_to_tokens):
    tokens = parse_to_tokens("hello\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\nworld"
