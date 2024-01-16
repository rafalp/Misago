import pytest

VALID_UNDERSCORE = (
    "world",
    "two worlds",
    "two_worlds",
    "two__worlds",
    "#words (with) symbols!",
)


@pytest.mark.parametrize("text", VALID_UNDERSCORE)
def test_emphasis_underscore(parse_markup, text):
    result = parse_markup(f"Hello _{text}_.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "emphasis-underscore",
                    "children": [{"type": "text", "text": text}],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_emphasis_underscore_with_line_break(parse_markup):
    result = parse_markup(f"Hello _lorem\nipsum_.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "emphasis-underscore",
                    "children": [
                        {"type": "text", "text": "lorem"},
                        {"type": "line-break"},
                        {"type": "text", "text": "ipsum"},
                    ],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_emphasis_underscores_next_to_each_other(parse_markup):
    result = parse_markup(f"Hello _lorem_ _ipsum_.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "emphasis-underscore",
                    "children": [{"type": "text", "text": "lorem"}],
                },
                {"type": "text", "text": " "},
                {
                    "type": "emphasis-underscore",
                    "children": [{"type": "text", "text": "ipsum"}],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


INVALID_EMPHASIS_UNDERSCORE = (
    "_lorem_ipsum",
    "lorem_ips_um",
    "lorem_ipsum_",
)


@pytest.mark.parametrize("text", INVALID_EMPHASIS_UNDERSCORE)
def test_emphasis_underscore_invalid_patterns(parse_markup, text):
    result = parse_markup(f"Hello {text}.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": f"Hello {text}."},
            ],
        }
    ]


@pytest.mark.parametrize("text", VALID_UNDERSCORE)
def test_strong_underscore(parse_markup, text):
    result = parse_markup(f"Hello __{text}__.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strong-underscore",
                    "children": [{"type": "text", "text": text}],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_strong_underscore_with_line_break(parse_markup):
    result = parse_markup(f"Hello __lorem\nipsum__.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strong-underscore",
                    "children": [
                        {"type": "text", "text": "lorem"},
                        {"type": "line-break"},
                        {"type": "text", "text": "ipsum"},
                    ],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_strong_underscores_next_to_each_other(parse_markup):
    result = parse_markup(f"Hello __lorem__ __ipsum__.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strong-underscore",
                    "children": [{"type": "text", "text": "lorem"}],
                },
                {"type": "text", "text": " "},
                {
                    "type": "strong-underscore",
                    "children": [{"type": "text", "text": "ipsum"}],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


INVALID_STRONG_UNDERSCORE = (
    "__lorem__ipsum",
    "lorem__ips__um",
    "lorem__ipsum__",
)


@pytest.mark.parametrize("text", INVALID_STRONG_UNDERSCORE)
def test_strong_underscore_invalid_patterns(parse_markup, text):
    result = parse_markup(f"Hello {text}.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": f"Hello {text}."},
            ],
        }
    ]
