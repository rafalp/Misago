import pytest

PATTERNS = (
    (
        "paragraph",
        "paragraph",
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "paragraph"}],
        },
    ),
    (
        "setex heading level 1",
        "heading\n====",
        {
            "type": "heading-setex",
            "level": 1,
            "children": [{"type": "text", "text": "heading"}],
        },
    ),
    (
        "setex heading level 2",
        "heading\n----",
        {
            "type": "heading-setex",
            "level": 2,
            "children": [{"type": "text", "text": "heading"}],
        },
    ),
    (
        "heading",
        "# heading",
        {
            "type": "heading",
            "level": 1,
            "children": [{"type": "text", "text": "heading"}],
        },
    ),
    (
        "thematic break bbcode",
        "[hr]",
        {"type": "thematic-break-bbcode"},
    ),
    (
        "thematic break dashes",
        "- - -",
        {"type": "thematic-break"},
    ),
    (
        "thematic break asterisks",
        "* * *",
        {"type": "thematic-break"},
    ),
)

PATTERNS_IDS = tuple(pattern[0] for pattern in PATTERNS)


@pytest.mark.parametrize("separator", ("\n", "\n\n"))
@pytest.mark.parametrize("second_pattern", PATTERNS, ids=PATTERNS_IDS)
@pytest.mark.parametrize("first_pattern", PATTERNS, ids=PATTERNS_IDS)
def test_block_patterns(parse_markup, first_pattern, second_pattern, separator):
    _, first_markdown, first_ast = first_pattern
    _, second_markdown, second_ast = second_pattern
    expected_result = get_expected_ast(first_ast, second_ast, separator)

    assert (
        parse_markup(f"{first_markdown}{separator}{second_markdown}") == expected_result
    )


THEMATIC_BREAK = ("thematic-break", "thematic-break-bbcode")


def get_expected_ast(ast, other_ast, separator):
    if (
        ast["type"] == "paragraph"
        and ast["type"] == other_ast["type"]
        and separator == "\n"
    ):
        # Only double newline character (or more) is a valid paragraph separator
        return [
            {
                "type": "paragraph",
                "children": [
                    {"type": "text", "text": "paragraph"},
                    {"type": "line-break"},
                    {"type": "text", "text": "paragraph"},
                ],
            },
        ]

    if ast["type"] in THEMATIC_BREAK and other_ast["type"] in THEMATIC_BREAK:
        # Multiple thematic breaks are combined into one
        return [ast]

    return [ast, other_ast]
