from ..factory import create_parser
from ..metadata import get_tokens_metadata
from ..tokenizer import tokenize


def test_get_tokens_metadata_returns_empty_metadata_for_plain_message():
    parser = create_parser()
    tokens = tokenize(parser, "lorem ipsum dolor met")
    metadata = get_tokens_metadata(tokens)
    assert metadata == {}


def test_get_tokens_metadata_returns_embedded_attachments():
    parser = create_parser()
    tokens = tokenize(parser, "<attachment=name.png:42>")
    metadata = get_tokens_metadata(tokens)
    assert metadata == {"attachments": [42]}


def test_get_tokens_metadata_returns_quoted_post():
    parser = create_parser()
    tokens = tokenize(parser, "[quote=User, post:123]lorem ipsum[/quote]")
    metadata = get_tokens_metadata(tokens)
    assert metadata == {"posts": [123]}


def test_get_tokens_metadata_returns_mentions():
    parser = create_parser()
    tokens = tokenize(parser, "lorem @Hello ipsum @Bob")
    metadata = get_tokens_metadata(tokens)
    assert metadata == {"mentions": ["bob", "hello"]}
