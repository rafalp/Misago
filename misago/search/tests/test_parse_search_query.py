from ..query import (
    SearchQueryAnd,
    SearchQueryKeyword,
    SearchQueryNot,
    SearchQueryOr,
    SearchQueryPhrase,
    parse_search_query,
)


def test_parse_search_query_parses_single_keyword():
    result = parse_search_query("keyword")

    assert result == SearchQueryKeyword(value="keyword")


def test_parse_search_query_parses_two_keywords():
    result = parse_search_query("lorem ipsum")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
        ],
    )


def test_parse_search_query_parses_three_keywords():
    result = parse_search_query("lorem ipsum dolor")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
            SearchQueryKeyword(value="dolor"),
        ],
    )


def test_parse_search_query_parses_phrase():
    result = parse_search_query("'lorem ipsum'")

    assert result == SearchQueryPhrase(value="lorem ipsum")


def test_parse_search_query_parses_two_phrases():
    result = parse_search_query("'lorem ipsum' 'dolor met'")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryPhrase(value="lorem ipsum"),
            SearchQueryPhrase(value="dolor met"),
        ],
    )


def test_parse_search_query_parses_three_phrases():
    result = parse_search_query("'lorem ipsum' 'dolor met' 'sit amet'")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryPhrase(value="lorem ipsum"),
            SearchQueryPhrase(value="dolor met"),
            SearchQueryPhrase(value="sit amet"),
        ],
    )


def test_parse_search_query_parses_single_not_keyword():
    result = parse_search_query("-keyword")

    assert result == SearchQueryNot(
        value=SearchQueryKeyword("keyword"),
    )


def test_parse_search_query_parses_two_or_keywords():
    result = parse_search_query("lorem | ipsum")

    assert result == SearchQueryOr(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
        ],
    )


def test_parse_search_query_parses_three_or_keywords():
    result = parse_search_query("lorem | ipsum | dolor")

    assert result == SearchQueryOr(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
            SearchQueryKeyword(value="dolor"),
        ],
    )


def test_parse_search_query_parses_single_not_phrase():
    result = parse_search_query("-'lorem ipsum'")

    assert result == SearchQueryNot(
        value=SearchQueryPhrase("lorem ipsum"),
    )


def test_parse_search_query_parses_two_or_phrases():
    result = parse_search_query("'lorem ipsum' | 'dolor met'")

    assert result == SearchQueryOr(
        value=[
            SearchQueryPhrase(value="lorem ipsum"),
            SearchQueryPhrase(value="dolor met"),
        ],
    )


def test_parse_search_query_parses_three_or_phrases():
    result = parse_search_query("'lorem ipsum' | 'dolor met' | 'sit amet'")

    assert result == SearchQueryOr(
        value=[
            SearchQueryPhrase(value="lorem ipsum"),
            SearchQueryPhrase(value="dolor met"),
            SearchQueryPhrase(value="sit amet"),
        ],
    )


def test_parse_search_query_parses_two_keywords_and_not_phrase():
    result = parse_search_query("lorem ipsum -'lorem ipsum'")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
            SearchQueryNot(
                value=SearchQueryPhrase(value="lorem ipsum"),
            ),
        ],
    )


def test_parse_search_query_parses_two_keywords_or_two_keywords():
    result = parse_search_query("(lorem ipsum) | (dolor met)")

    assert result == SearchQueryOr(
        value=[
            SearchQueryAnd(
                value=[
                    SearchQueryKeyword(value="lorem"),
                    SearchQueryKeyword(value="ipsum"),
                ],
            ),
            SearchQueryAnd(
                value=[
                    SearchQueryKeyword(value="dolor"),
                    SearchQueryKeyword(value="met"),
                ],
            ),
        ],
    )
