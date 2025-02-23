import pytest

PATTERNS = (
    (
        "paragraph",
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "paragraph"}],
        },
    ),
    (
        "# heading",
        {
            "type": "heading",
            "level": 1,
            "children": [{"type": "text", "text": "heading"}],
        },
    ),
    (
        "[hr]",
        {"type": "thematic-break-bbcode"},
    ),
    (
        "- - -",
        {"type": "thematic-break"},
    ),
    (
        "* * *",
        {"type": "thematic-break"},
    ),
)


@pytest.mark.parametrize("first_pattern", PATTERNS)
@pytest.mark.parametrize("second_pattern", PATTERNS)
@pytest.mark.parametrize("separator", ("\n", "\n\n"))
def test_block_patterns(parse_markup, first_pattern, second_pattern, separator):
    first_markdown, first_ast = first_pattern
    second_markdown, second_ast = second_pattern
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
