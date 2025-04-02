from ..factory import create_parser
from ..plaintext import render_plaintext
from ..tokenizer import tokenize


def test_render_plaintext_renders_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "hello")
    assert render_plaintext(tokens) == "hello"


def test_render_plaintext_renders_two_paragraphs():
    parser = create_parser()
    tokens = tokenize(parser, "hello\n\nworld")
    assert render_plaintext(tokens) == "hello\n\nworld"


def test_render_plaintext_renders_header_and_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "# hello\n\nworld")
    assert render_plaintext(tokens) == "hello\n\nworld"


def test_render_plaintext_renders_setex_header_and_paragraph():
    parser = create_parser()
    tokens = tokenize(parser, "hello\n=====\n\nworld")
    assert render_plaintext(tokens) == "hello\n\nworld"


def test_render_plaintext_renders_blockquote():
    parser = create_parser()
    tokens = tokenize(parser, "> hello")
    assert render_plaintext(tokens) == "hello"


def test_render_plaintext_renders_quote_bbcode():
    parser = create_parser()
    tokens = tokenize(parser, "[quote]hello[/quote]")
    assert render_plaintext(tokens) == "hello"


def test_render_plaintext_renders_quote_bbcode_with_info():
    parser = create_parser()
    tokens = tokenize(parser, "[quote=info]hello[/quote]")
    assert render_plaintext(tokens) == "info:\n\nhello"


def test_render_plaintext_renders_quote_bbcode_with_user():
    parser = create_parser()
    tokens = tokenize(parser, "[quote=User, post: 123]hello[/quote]")
    assert render_plaintext(tokens) == "User:\n\nhello"


def test_render_plaintext_renders_spoiler_bbcode():
    parser = create_parser()
    tokens = tokenize(parser, "[spoiler]hello[/spoiler]")
    assert render_plaintext(tokens) == "hello"


def test_render_plaintext_renders_spoiler_bbcode_with_info():
    parser = create_parser()
    tokens = tokenize(parser, "[spoiler=info]hello[/spoiler]")
    assert render_plaintext(tokens) == "info:\n\nhello"


def test_render_plaintext_renders_soft_linebreak():
    parser = create_parser()
    tokens = tokenize(parser, "hello\nworld")
    assert render_plaintext(tokens) == "hello\nworld"
