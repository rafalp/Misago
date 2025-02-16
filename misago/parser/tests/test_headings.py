from ...test import disable_parser_clean_ast


@disable_parser_clean_ast
def test_empty_atx_heading(parse_markup):
    result = parse_markup("#")
    assert result == [
        {
            "type": "heading",
            "level": 1,
            "children": [],
        }
    ]


def test_atx_heading_with_text(parse_markup):
    result = parse_markup("# Hello World!")
    assert result == [
        {
            "type": "heading",
            "level": 1,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_atx_heading_second_level(parse_markup):
    result = parse_markup("## Hello World!")
    assert result == [
        {
            "type": "heading",
            "level": 2,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_atx_heading_third_level(parse_markup):
    result = parse_markup("### Hello World!")
    assert result == [
        {
            "type": "heading",
            "level": 3,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_atx_heading_fourth_level(parse_markup):
    result = parse_markup("#### Hello World!")
    assert result == [
        {
            "type": "heading",
            "level": 4,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_atx_heading_fifth_level(parse_markup):
    result = parse_markup("##### Hello World!")
    assert result == [
        {
            "type": "heading",
            "level": 5,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_atx_heading_sixth_level(parse_markup):
    result = parse_markup("###### Hello World!")
    assert result == [
        {
            "type": "heading",
            "level": 6,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_atx_heading_text_whitespace_is_stripped(parse_markup):
    result = parse_markup("#     Hello World!   ")
    assert result == [
        {
            "type": "heading",
            "level": 1,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_atx_heading_breaks_paragraphs(parse_markup):
    result = parse_markup("Lorem ipsum\n# Dolor met\nSit amet")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum"},
            ],
        },
        {
            "type": "heading",
            "level": 1,
            "children": [
                {"type": "text", "text": "Dolor met"},
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Sit amet"},
            ],
        },
    ]


def test_setex_heading(parse_markup):
    result = parse_markup("Hello World!\n=")
    assert result == [
        {
            "type": "heading-setex",
            "level": 1,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_setex_heading_second_level(parse_markup):
    result = parse_markup("Hello World!\n-")
    assert result == [
        {
            "type": "heading-setex",
            "level": 2,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_setex_heading_text_whitespace_is_stripped(parse_markup):
    result = parse_markup("  Hello World!    \n-")
    assert result == [
        {
            "type": "heading-setex",
            "level": 2,
            "children": [
                {"type": "text", "text": "Hello World!"},
            ],
        }
    ]


def test_setex_heading_breaks_paragraphs(parse_markup):
    result = parse_markup("Lorem ipsum\nDolor met\n===\nSit amet")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum"},
            ],
        },
        {
            "type": "heading-setex",
            "level": 1,
            "children": [
                {"type": "text", "text": "Dolor met"},
            ],
        },
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Sit amet"},
            ],
        },
    ]
