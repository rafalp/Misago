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


def test_emphasis_underscore_without_content_is_removed(parse_markup):
    result = parse_markup(f"Hello __.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello ."},
            ],
        }
    ]


def test_emphasis_underscore_with_only_whitespaces_is_removed(parse_markup):
    result = parse_markup(f"Hello _  \n  _.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello ."},
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


def test_strong_underscores_without_content_is_removed(parse_markup):
    result = parse_markup(f"Hello ____.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello ."},
            ],
        }
    ]


def test_strong_underscores_with_whitespaces_only_is_removed(parse_markup):
    result = parse_markup(f"Hello __  \n  __.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello ."},
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


def test_strikethrough(parse_markup):
    result = parse_markup(f"Hello ~~lorem~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "lorem"},
                    ],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_strikethrough_beginning_of_word(parse_markup):
    result = parse_markup(f"Hello ~~lo~~rem.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "lo"},
                    ],
                },
                {"type": "text", "text": "rem."},
            ],
        }
    ]


def test_strikethrough_inside_a_word(parse_markup):
    result = parse_markup(f"Hello lo~~r~~em.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello lo"},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "r"},
                    ],
                },
                {"type": "text", "text": "em."},
            ],
        }
    ]


def test_strikethrough_end_of_word(parse_markup):
    result = parse_markup(f"Hello lo~~rem~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello lo"},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "rem"},
                    ],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_strikethrough_two_words(parse_markup):
    result = parse_markup(f"Hello ~~lorem ipsum~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "lorem ipsum"},
                    ],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_strikethrough_with_line_break(parse_markup):
    result = parse_markup(f"Hello ~~lorem\nipsum~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strikethrough",
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


def test_strikethrough_with_symbols(parse_markup):
    result = parse_markup(f"Hello ~~(lorem ipsum)~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "(lorem ipsum)"},
                    ],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_strikethrough_next_to_another(parse_markup):
    result = parse_markup(f"Hello ~~lorem~~ ~~ipsum~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "lorem"},
                    ],
                },
                {"type": "text", "text": " "},
                {
                    "type": "strikethrough",
                    "children": [
                        {"type": "text", "text": "ipsum"},
                    ],
                },
                {"type": "text", "text": "."},
            ],
        }
    ]


def test_strikethrough_without_content_is_removed(parse_markup):
    result = parse_markup(f"Hello ~~~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello ."},
            ],
        }
    ]


def test_strikethrough_with_whitespaces_only_is_removed(parse_markup):
    result = parse_markup(f"Hello ~~  \n  ~~.")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello ."},
            ],
        }
    ]
