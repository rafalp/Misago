def test_code_bbcode_can_be_one_liner(parse_markup):
    result = parse_markup(
        """
        [code]alert("hello!")[/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": 'alert("hello!")',
        }
    ]


def test_code_bbcode_can_be_multiline(parse_markup):
    result = parse_markup(
        """
        [code]
        alert("hello!")
        alert("world!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_dedents_content(parse_markup):
    result = parse_markup(
        """
        [code]
          alert("hello!")
          alert("world!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_trims_content(parse_markup):
    result = parse_markup(
        """
        [code]

          alert("hello!")
          alert("world!")

        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_supports_syntax(parse_markup):
    result = parse_markup(
        """
        [code=python]
        alert("hello!")
        alert("world!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": "python",
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_trims_syntax(parse_markup):
    result = parse_markup(
        """
        [code=  python   ]
        alert("hello!")
        alert("world!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": "python",
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_trims_syntax_quotes(parse_markup):
    result = parse_markup(
        """
        [code="  python  "]
        alert("hello!")
        alert("world!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": "python",
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_trims_syntax_single_quotes(parse_markup):
    result = parse_markup(
        """
        [code='  python  ']
        alert("hello!")
        alert("world!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": "python",
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_unescapes_info(parse_markup):
    result = parse_markup(
        """
        [code="Failing \"feature\" example"]
        alert("hello!")
        alert("world!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": 'Failing "feature" example',
            "syntax": None,
            "code": 'alert("hello!")\nalert("world!")',
        }
    ]


def test_code_bbcode_preserves_escaping_characters(parse_markup):
    result = parse_markup(
        """
        [code]
        alert("hel\+lo!")
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": 'alert("hel\+lo!")',
        }
    ]


def test_code_bbcode_preserves_inline_code(parse_markup):
    result = parse_markup(
        """
        [code]
        `text`
        [/code]
        """
    )
    assert result == [
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": "`text`",
        }
    ]


def test_code_bbcode_can_be_mixed_with_other_blocks(parse_markup):
    result = parse_markup(
        """
        Here is the code:

        [code]
        1 + 3
        [/code]
        It's cool!
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Here is the code:"}],
        },
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": "1 + 3",
        },
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "It's cool!"}],
        },
    ]


def test_code_bbcode_can_be_used_next_to_each_other(parse_markup):
    result = parse_markup(
        """
        Here is the code:

        [code]
        1 + 3
        [/code][code]
        5 x 3
        [/code]
        It's cool!
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Here is the code:"}],
        },
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": "1 + 3",
        },
        {
            "type": "code-bbcode",
            "info": None,
            "syntax": None,
            "code": "5 x 3",
        },
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "It's cool!"}],
        },
    ]
