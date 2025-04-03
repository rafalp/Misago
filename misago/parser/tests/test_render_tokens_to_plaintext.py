from ..factory import create_parser
from ..plaintext import render_tokens_to_plaintext
from ..tokenizer import tokenize


def test_render_tokens_to_plaintext_renders_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "hello")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_two_paragraphs():
    parser = create_parser()
    tokens = tokenize(parser, "hello\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


def test_render_tokens_to_plaintext_renders_header_and_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "# hello\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


def test_render_tokens_to_plaintext_renders_setex_header_and_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "hello\n=====\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


def test_render_tokens_to_plaintext_renders_code():
    parser = create_parser()
    tokens = tokenize(parser, "    hello\n    world")
    assert render_tokens_to_plaintext(tokens) == "hello\nworld"


def test_render_tokens_to_plaintext_renders_fenced_code():
    parser = create_parser()
    tokens = tokenize(parser, "```\nhello")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_info():
    parser = create_parser()
    tokens = tokenize(parser, "```info\nhello")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_syntax():
    parser = create_parser()
    tokens = tokenize(parser, "```php\nhello")
    assert render_tokens_to_plaintext(tokens) == "php:\nhello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_info_and_syntax():
    parser = create_parser()
    tokens = tokenize(parser, "```info, syntax: php\nhello")
    assert render_tokens_to_plaintext(tokens) == "info, php:\nhello"


def test_render_tokens_to_plaintext_renders_code_bbcode():
    parser = create_parser()
    tokens = tokenize(parser, "[code]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_code_bbcode_with_info():
    parser = create_parser()
    tokens = tokenize(parser, "[code=info]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_code_bbcode_with_syntax():
    parser = create_parser()
    tokens = tokenize(parser, "[code=php]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "php:\nhello"


def test_render_tokens_to_plaintext_renders_code_bbcode_with_info_and_syntax():
    parser = create_parser()
    tokens = tokenize(parser, "[code=info, syntax: php]\nhello\n[/code]")
    assert render_tokens_to_plaintext(tokens) == "info, php:\nhello"


def test_render_tokens_to_plaintext_renders_blockquote():
    parser = create_parser()
    tokens = tokenize(parser, "> hello")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_quote_bbcode():
    parser = create_parser()
    tokens = tokenize(parser, "[quote]hello[/quote]")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_quote_bbcode_with_info():
    parser = create_parser()
    tokens = tokenize(parser, "[quote=info]hello[/quote]")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_quote_bbcode_with_user():
    parser = create_parser()
    tokens = tokenize(parser, "[quote=User, post: 123]hello[/quote]")
    assert render_tokens_to_plaintext(tokens) == "User, #123:\nhello"


def test_render_tokens_to_plaintext_renders_spoiler_bbcode():
    parser = create_parser()
    tokens = tokenize(parser, "[spoiler]hello[/spoiler]")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_spoiler_bbcode_with_info():
    parser = create_parser()
    tokens = tokenize(parser, "[spoiler=info]hello[/spoiler]")
    assert render_tokens_to_plaintext(tokens) == "info:\nhello"


def test_render_tokens_to_plaintext_renders_ordered_list():
    parser = create_parser()
    tokens = tokenize(parser, "2. lorem\n3. ipsum")
    assert render_tokens_to_plaintext(tokens) == "2. lorem\n3. ipsum"


def test_render_tokens_to_plaintext_renders_bullet_list():
    parser = create_parser()
    tokens = tokenize(parser, "- lorem\n- ipsum")
    assert render_tokens_to_plaintext(tokens) == "- lorem\n- ipsum"


def test_render_tokens_to_plaintext_renders_ordered_list_with_nested_ordered_list():
    parser = create_parser()
    tokens = tokenize(parser, "2. lorem\n   1. ipsum\n   2. dolor\n3. met")
    assert render_tokens_to_plaintext(tokens) == (
        "2. lorem" "\n2. 1. ipsum" "\n2. 2. dolor" "\n3. met"
    )


def test_render_tokens_to_plaintext_renders_ordered_list_with_nested_bullet_list():
    parser = create_parser()
    tokens = tokenize(parser, "2. lorem\n   - ipsum\n   - dolor\n3. met")
    assert render_tokens_to_plaintext(tokens) == (
        "2. lorem" "\n2. - ipsum" "\n2. - dolor" "\n3. met"
    )


def test_render_tokens_to_plaintext_renders_bullet_list_with_nested_ordered_list():
    parser = create_parser()
    tokens = tokenize(parser, "- lorem\n  1. ipsum\n  2. dolor\n- met")
    assert render_tokens_to_plaintext(tokens) == (
        "- lorem" "\n- 1. ipsum" "\n- 2. dolor" "\n- met"
    )


def test_render_tokens_to_plaintext_renders_bullet_list_with_nested_bullet_list():
    parser = create_parser()
    tokens = tokenize(parser, "- lorem\n  - ipsum\n  - dolor\n- met")
    assert render_tokens_to_plaintext(tokens) == (
        "- lorem" "\n- - ipsum" "\n- - dolor" "\n- met"
    )


def test_render_tokens_to_plaintext_renders_attachments():
    parser = create_parser()
    tokens = tokenize(parser, "<attachment=image.png:1><attachment=video.mp4:2>")
    assert render_tokens_to_plaintext(tokens) == "image.png\nvideo.mp4"


def test_render_tokens_to_plaintext_renders_code_inline():
    parser = create_parser()
    tokens = tokenize(parser, "Hello, `inline`")
    assert render_tokens_to_plaintext(tokens) == "Hello, inline"


def test_render_tokens_to_plaintext_renders_mention():
    parser = create_parser()
    tokens = tokenize(parser, "Hello, @Username")
    assert render_tokens_to_plaintext(tokens) == "Hello, @Username"


def test_render_tokens_to_plaintext_renders_soft_linebreak():
    parser = create_parser()
    tokens = tokenize(parser, "hello\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\nworld"
