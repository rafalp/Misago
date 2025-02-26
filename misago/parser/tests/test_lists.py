import pytest

CASES = (
    (
        "single item dash",
        "- item",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "single item plus",
        "+ item",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "+",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "single item asterisk",
        "* item",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "*",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "single item ordered dot",
        "1. item",
        {
            "type": "list",
            "ordered": True,
            "start": None,
            "delimiter": ".",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "single item ordered parenthesis",
        "1) item",
        {
            "type": "list",
            "ordered": True,
            "start": None,
            "delimiter": ")",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "single item ordered with zero start",
        "0) item",
        {
            "type": "list",
            "ordered": True,
            "start": "0",
            "delimiter": ")",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "single item ordered with start",
        "7) item",
        {
            "type": "list",
            "ordered": True,
            "start": "7",
            "delimiter": ")",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "single indented item dash",
        "   - item",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "list item with softbreak",
        "   - item\nnext line",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                                {"type": "softbreak"},
                                {"type": "text", "text": "next line"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "indented list item with softbreak, second line indented",
        "   - item\n  next line",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item"},
                                {"type": "softbreak"},
                                {"type": "text", "text": "next line"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "indented list item with two paragraphs",
        "   - paragraph1\n\n     paragraph2",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph1"},
                            ],
                        },
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph2"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "list item with two paragraphs",
        "- paragraph1\n\n  paragraph2",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph1"},
                            ],
                        },
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph2"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "list item with two paragraphs and two softbreaks",
        "- paragraph1\nline1\n\n  paragraph2\nline2",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph1"},
                                {"type": "softbreak"},
                                {"type": "text", "text": "line1"},
                            ],
                        },
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph2"},
                                {"type": "softbreak"},
                                {"type": "text", "text": "line2"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "list item with three paragraphs",
        "- paragraph1\n\n  paragraph2\n\n  paragraph3",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph1"},
                            ],
                        },
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph2"},
                            ],
                        },
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "paragraph3"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "list with two items",
        "- item1\n- item2",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item1"},
                            ],
                        },
                    ],
                },
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item2"},
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "list with nested list",
        "- item1\n  - item2",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"type": "text", "text": "item1"},
                            ],
                        },
                        {
                            "type": "list",
                            "ordered": False,
                            "start": None,
                            "delimiter": "-",
                            "tight": True,
                            "children": [
                                {
                                    "type": "list-item",
                                    "children": [
                                        {
                                            "type": "paragraph",
                                            "children": [
                                                {"type": "text", "text": "item2"},
                                            ],
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ),
    (
        "test_list_unescapes_items",
        "- \*Lorem\*",
        {
            "type": "list",
            "ordered": False,
            "start": None,
            "delimiter": "-",
            "tight": True,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {
                            "type": "paragraph",
                            "children": [
                                {
                                    "type": "text",
                                    "text": "*Lorem*",
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    ),
)

CASES_IDS = tuple(case[0] for case in CASES)


@pytest.mark.parametrize("case", CASES, ids=CASES_IDS)
def test_lists(parse_markup, case):
    _, markdown, expected_ast = case

    if not isinstance(expected_ast, list):
        expected_ast = [expected_ast]

    assert parse_markup(markdown) == expected_ast
