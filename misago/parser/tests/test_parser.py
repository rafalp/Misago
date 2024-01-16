from textwrap import dedent

from ..parser import Parser


def parse(value: str) -> list[dict]:
    return Parser()(dedent(value).strip())


def test_parser_parses_single_paragraph():
    result = parse("Hello world!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello world!"},
            ],
        }
    ]


def test_parser_parses_two_paragraphs():
    result = parse("First paragraph.\n\nSecond paragraph.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "First paragraph."},
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Second paragraph."},
            ],
        },
    ]


def test_parser_parses_skips_extra_linebreaks_between_blocks():
    result = parse("First paragraph.\n\n\n\nSecond paragraph.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "First paragraph."},
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Second paragraph."},
            ],
        },
    ]


def test_parser_parses_line_breaks():
    result = parse("Paragraph with\na line break.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Paragraph with"},
                {"type": "line-break"},
                {"type": "text", "text": "a line break."},
            ],
        },
    ]


def test_parser_parses_line_breaks_surrounded_by_spaces():
    result = parse("Paragraph with  \n   a line break.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Paragraph with"},
                {"type": "line-break"},
                {"type": "text", "text": "a line break."},
            ],
        },
    ]
