from ..postprocessors import CleanASTPostProcessor

processor = CleanASTPostProcessor()


def test_clean_ast_post_processor_removes_attachment_from_paragraph(parse_markup):
    ast = parse_markup("<attachment=file.txt:123>")
    assert ast == [
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "file.txt",
                    "slug": "file-txt",
                    "id": 123,
                },
            ],
        }
    ]


def test_clean_ast_post_processor_splits_paragraph_with_attachment(parse_markup):
    ast = parse_markup("Lorem<attachment=file.txt:123>Ipsum")
    assert ast == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem"},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "file.txt",
                    "slug": "file-txt",
                    "id": 123,
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Ipsum"},
            ],
        },
    ]


def test_clean_ast_post_processor_splits_paragraph_with_two_attachments(parse_markup):
    ast = parse_markup(
        "Lorem<attachment=file.txt:123>Ipsum<attachment=file.txt:123>Dolor"
    )
    assert ast == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem"},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "file.txt",
                    "slug": "file-txt",
                    "id": 123,
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Ipsum"},
            ],
        },
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "file.txt",
                    "slug": "file-txt",
                    "id": 123,
                },
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Dolor"},
            ],
        },
    ]


def test_clean_ast_post_processor_removes_empty_node(parse_markup):
    ast = parse_markup("#\n\nLorem")
    assert ast == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem"},
            ],
        },
    ]
