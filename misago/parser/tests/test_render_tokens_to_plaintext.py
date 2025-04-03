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
    assert render_tokens_to_plaintext(tokens) == "info:\n\nhello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_syntax():
    parser = create_parser()
    tokens = tokenize(parser, "```php\nhello")
    assert render_tokens_to_plaintext(tokens) == "php:\n\nhello"


def test_render_tokens_to_plaintext_renders_fenced_code_with_info_and_syntax():
    parser = create_parser()
    tokens = tokenize(parser, "```info, syntax: php\nhello")
    assert render_tokens_to_plaintext(tokens) == "info, php:\n\nhello"


def test_render_tokens_to_plaintext_renders_header_and_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "# hello\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


def test_render_tokens_to_plaintext_renders_setex_header_and_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "hello\n=====\n\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\n\nworld"


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
    assert render_tokens_to_plaintext(tokens) == "info:\n\nhello"


def test_render_tokens_to_plaintext_renders_quote_bbcode_with_user():
    parser = create_parser()
    tokens = tokenize(parser, "[quote=User, post: 123]hello[/quote]")
    assert render_tokens_to_plaintext(tokens) == "User:\n\nhello"


def test_render_tokens_to_plaintext_renders_spoiler_bbcode():
    parser = create_parser()
    tokens = tokenize(parser, "[spoiler]hello[/spoiler]")
    assert render_tokens_to_plaintext(tokens) == "hello"


def test_render_tokens_to_plaintext_renders_spoiler_bbcode_with_info():
    parser = create_parser()
    tokens = tokenize(parser, "[spoiler=info]hello[/spoiler]")
    assert render_tokens_to_plaintext(tokens) == "info:\n\nhello"


def test_render_tokens_to_plaintext_renders_ordered_list():
    parser = create_parser()
    tokens = tokenize(parser, "paragraph\n\n1. lorem\n2. ipsum")
    assert render_tokens_to_plaintext(tokens) == "paragraph\n\n1. lorem\n2. ipsum"


def test_render_tokens_to_plaintext_renders_ordered_list_with_nested_ordered_list():
    parser = create_parser()
    tokens = tokenize(parser, "paragraph\n\n1. lorem\n2. ipsum\n  1. nested")
    assert render_tokens_to_plaintext(tokens) == "paragraph\n\n1. lorem\n2. ipsum"


def test_render_tokens_to_plaintext_renders_attachments():
    parser = create_parser()
    tokens = tokenize(parser, "<attachment=image.png:1><attachment=video.mp4:2>")
    assert render_tokens_to_plaintext(tokens) == "image.png\nvideo.mp4"


def test_render_tokens_to_plaintext_renders_soft_linebreak():
    parser = create_parser()
    tokens = tokenize(parser, "hello\nworld")
    assert render_tokens_to_plaintext(tokens) == "hello\nworld"


def test_render_tokens_to_plaintext_renders_mention():
    parser = create_parser()
    tokens = tokenize(parser, "@Username")
    assert render_tokens_to_plaintext(tokens) == "@Username"
