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
        "fenced code",
        '```\nalert("Hello world!")\n```',
        {
            "type": "code",
            "syntax": None,
            "code": 'alert("Hello world!")',
        },
    ),
    (
        "fenced code alternate",
        '~~~\nalert("Hello world!")\n~~~',
        {
            "type": "code",
            "syntax": None,
            "code": 'alert("Hello world!")',
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
    (
        "single item dash list",
        "- item",
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item"},
                    ],
                    "lists": [],
                },
            ],
        },
    ),
    (
        "multiple items dash list",
        "- item1\n- item2\n- item3",
        {
            "type": "list",
            "ordered": False,
            "sign": "-",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item1"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item2"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item3"},
                    ],
                    "lists": [],
                },
            ],
        },
    ),
    (
        "single item asterisk list",
        "* item",
        {
            "type": "list",
            "ordered": False,
            "sign": "*",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item"},
                    ],
                    "lists": [],
                },
            ],
        },
    ),
    (
        "multiple items asterisk list",
        "* item1\n* item2\n* item3",
        {
            "type": "list",
            "ordered": False,
            "sign": "*",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item1"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item2"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item3"},
                    ],
                    "lists": [],
                },
            ],
        },
    ),
    (
        "single item plus list",
        "+ item",
        {
            "type": "list",
            "ordered": False,
            "sign": "+",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item"},
                    ],
                    "lists": [],
                },
            ],
        },
    ),
    (
        "multiple items plus list",
        "+ item1\n+ item2\n+ item3",
        {
            "type": "list",
            "ordered": False,
            "sign": "+",
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item1"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item2"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item3"},
                    ],
                    "lists": [],
                },
            ],
        },
    ),
    (
        "single item ordered list",
        "1. item",
        {
            "type": "list",
            "ordered": True,
            "sign": None,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item"},
                    ],
                    "lists": [],
                },
            ],
        },
    ),
    (
        "multiple items ordered list",
        "1. item1\n2. item2\n3. item3",
        {
            "type": "list",
            "ordered": True,
            "sign": None,
            "children": [
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item1"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item2"},
                    ],
                    "lists": [],
                },
                {
                    "type": "list-item",
                    "children": [
                        {"type": "text", "text": "item3"},
                    ],
                    "lists": [],
                },
            ],
        },
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

    if (
        ast["type"] == "list"
        and ast["type"] == other_ast["type"]
        and ast["ordered"]
        and other_ast["ordered"]
        and separator == "\n"
    ):
        # Multiple lists of same type are combined into one
        return [
            {
                "type": "list",
                "ordered": True,
                "sign": None,
                "children": [
                    {
                        "type": "list-item",
                        "children": [
                            {"type": "text", "text": "item"},
                        ],
                        "lists": [],
                    },
                    {
                        "type": "list-item",
                        "children": [
                            {"type": "text", "text": "item"},
                        ],
                        "lists": [],
                    },
                ],
            },
        ]

    return [ast, other_ast]
