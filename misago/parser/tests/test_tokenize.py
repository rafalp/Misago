from ..factory import create_parser
from ..html import render_tokens_to_html
from ..tokenizer import tokenize


def test_tokenize_tokenizes_str():
    parser = create_parser()
    tokens = tokenize(parser, "hello")
    assert len(tokens) == 3
    assert render_tokens_to_html(parser, tokens) == "<p>hello</p>"
