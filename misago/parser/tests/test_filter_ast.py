from ..ast import filter_ast


def test_filter_ast_removes_blank_line_ast_from_between_paragraphs(markdown):
    result = markdown("Lorem ipsum\n\nDolor met")
    result = filter_ast(result)

    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "raw": "Lorem ipsum"}],
        },
        {
            "type": "paragraph",
            "children": [{"type": "text", "raw": "Dolor met"}],
        },
    ]


def test_filter_ast_removes_blank_line_ast_from_between_header_block_and_paragraph(
    markdown,
):
    result = markdown("# Lorem ipsum\n\nDolor met")
    result = filter_ast(result)

    assert result == [
        {
            "type": "heading",
            "attrs": {
                "level": 1,
            },
            "style": "axt",
            "children": [{"type": "text", "raw": "Lorem ipsum"}],
        },
        {
            "type": "paragraph",
            "children": [{"type": "text", "raw": "Dolor met"}],
        },
    ]


def test_filter_ast_removes_blank_line_ast_from_between_quoted_paragraphs(markdown):
    result = markdown("> Lorem ipsum\n> \n> Dolor met")
    result = filter_ast(result)

    assert result == [
        {
            "type": "block_quote",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "raw": "Lorem ipsum"}],
                },
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "raw": "Dolor met"}],
                },
            ],
        }
    ]
