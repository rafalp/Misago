from ..query import normalize_quotes


def test_normalize_quotes_normalizes_single_quotes():
    assert normalize_quotes("hello ’world’!") == "hello 'world'!"


def test_normalize_quotes_normalizes_double_quotes():
    assert normalize_quotes('hello "world"!') == "hello 'world'!"


def test_normalize_quotes_normalizes_polish_quotes():
    assert normalize_quotes("hello „world”!") == "hello 'world'!"
