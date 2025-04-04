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


def test_get_tokens_metadata_returns_highlight_code_for_fence_code_with_syntax():
    parser = create_parser()
    tokens = tokenize(parser, '```php\nhello("world")')
    metadata = get_tokens_metadata(tokens)
    assert metadata == {"highlight_code": True}


def test_get_tokens_metadata_returns_highlight_code_for_code_bbcode_with_syntax():
    parser = create_parser()
    tokens = tokenize(parser, '[code=php]\nhello("world")\n[/code]')
    metadata = get_tokens_metadata(tokens)
    assert metadata == {"highlight_code": True}


def test_get_tokens_metadata_returns_quoted_post():
    parser = create_parser()
    tokens = tokenize(parser, "[quote=User, post:123]lorem ipsum[/quote]")
    metadata = get_tokens_metadata(tokens)
    assert metadata == {"posts": [123]}


def test_get_tokens_metadata_returns_mentions(user):
    parser = create_parser()
    tokens = tokenize(parser, f"lorem @{user.username} ipsum @Bob")
    metadata = get_tokens_metadata(tokens)
    assert metadata == {"mentions": [user.id]}
