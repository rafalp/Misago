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


def test_parse_search_query_parses__keywords_and_not_keyword_or_two_keywords():
    result = parse_search_query("(lorem -ipsum) | (dolor met)")

    assert result == SearchQueryOr(
        value=[
            SearchQueryAnd(
                value=[
                    SearchQueryKeyword(value="lorem"),
                    SearchQueryNot(
                        value=SearchQueryKeyword(value="ipsum"),
                    ),
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


def test_parse_search_query_parses_keywords_and_not_keywords():
    result = parse_search_query("(lorem ipsum) -(dolor met)")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryAnd(
                value=[
                    SearchQueryKeyword(value="lorem"),
                    SearchQueryKeyword(value="ipsum"),
                ],
            ),
            SearchQueryNot(
                value=SearchQueryAnd(
                    value=[
                        SearchQueryKeyword(value="dolor"),
                        SearchQueryKeyword(value="met"),
                    ],
                ),
            ),
        ],
    )


def test_parse_search_query_parses_keywords_or_not_keywords():
    result = parse_search_query("(lorem ipsum) | -(dolor met)")

    assert result == SearchQueryOr(
        value=[
            SearchQueryAnd(
                value=[
                    SearchQueryKeyword(value="lorem"),
                    SearchQueryKeyword(value="ipsum"),
                ],
            ),
            SearchQueryNot(
                value=SearchQueryAnd(
                    value=[
                        SearchQueryKeyword(value="dolor"),
                        SearchQueryKeyword(value="met"),
                    ],
                ),
            ),
        ],
    )


def test_parse_search_query_parses_keywords_or_keywords():
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


def test_parse_search_query_parses_keywords_or_keywords_with_not_keyword():
    result = parse_search_query("(lorem ipsum) | (dolor met -elit)")

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
                    SearchQueryNot(
                        value=SearchQueryKeyword(value="elit"),
                    ),
                ],
            ),
        ],
    )


def test_parse_search_query_parses_keyword_group_or_keyword_group():
    result = parse_search_query("(lorem) | (ipsum)")

    assert result == SearchQueryOr(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
        ],
    )


def test_parse_search_query_parses_keyword_and_keyword_or_keyword():
    result = parse_search_query("lorem ipsum | dolor")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryOr(
                value=[
                    SearchQueryKeyword(value="ipsum"),
                    SearchQueryKeyword(value="dolor"),
                ],
            ),
        ],
    )


def test_parse_search_query_parses_keyword_and_keyword_or_keyword_or_keyword():
    result = parse_search_query("lorem ipsum | dolor | met")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryOr(
                value=[
                    SearchQueryKeyword(value="ipsum"),
                    SearchQueryKeyword(value="dolor"),
                    SearchQueryKeyword(value="met"),
                ],
            ),
        ],
    )


def test_parse_search_query_parses_keyword_or_keyword_or_keyword_and_keyword():
    result = parse_search_query("lorem | ipsum | dolor met")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryOr(
                value=[
                    SearchQueryKeyword(value="lorem"),
                    SearchQueryKeyword(value="ipsum"),
                    SearchQueryKeyword(value="dolor"),
                ],
            ),
            SearchQueryKeyword(value="met"),
        ],
    )


def test_parse_search_query_parses_keyword_or_keyword_or_keyword_and_keyword_group():
    result = parse_search_query("lorem | ipsum | (dolor met)")

    assert result == SearchQueryOr(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
            SearchQueryAnd(
                value=[
                    SearchQueryKeyword(value="dolor"),
                    SearchQueryKeyword(value="met"),
                ],
            ),
        ],
    )


def test_parse_search_query_parses_unclosed_group():
    result = parse_search_query("lorem -(dolor  met")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryNot(
                value=SearchQueryAnd(
                    value=[
                        SearchQueryKeyword(value="dolor"),
                        SearchQueryKeyword(value="met"),
                    ],
                ),
            ),
        ],
    )


def test_parse_search_query_parses_multiple_unclosed_groups():
    result = parse_search_query("lorem -((((dolor  met")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryNot(
                value=SearchQueryAnd(
                    value=[
                        SearchQueryKeyword(value="dolor"),
                        SearchQueryKeyword(value="met"),
                    ],
                ),
            ),
        ],
    )


def test_parse_search_query_parses_unopened_group():
    result = parse_search_query("lorem -dolor) met)")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryNot(
                value=SearchQueryKeyword(value="dolor"),
            ),
            SearchQueryKeyword(value="met"),
        ],
    )


def test_parse_search_query_parses_empty_phrase():
    result = parse_search_query("lorem '  ' met")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="met"),
        ],
    )


def test_parse_search_query_parses_not_before_or():
    result = parse_search_query("lorem -| met)")

    assert result == SearchQueryOr(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="met"),
        ],
    )


def test_parse_search_query_parses_not_before_empty_group():
    result = parse_search_query("lorem -()")

    assert result == SearchQueryKeyword(value="lorem")


def test_parse_search_query_parses_not_at_query_end():
    result = parse_search_query("lorem -")

    assert result == SearchQueryKeyword(value="lorem")


def test_parse_search_query_parses_not_empty_phrase():
    result = parse_search_query("lorem -'   ' ipsum")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
        ],
    )


def test_parse_search_query_parses_or_empty_phrase():
    result = parse_search_query("lorem | '   ' | ipsum")

    assert result == SearchQueryOr(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
        ],
    )


def test_parse_search_query_parses_group_or_empty_phrase():
    result = parse_search_query("lorem ('   ' | ipsum)")

    assert result == SearchQueryAnd(
        value=[
            SearchQueryKeyword(value="lorem"),
            SearchQueryKeyword(value="ipsum"),
        ],
    )
