def test_fenced_code_supports_backticks(parse_markup):
    result = parse_markup(
        """
        ```
        print("hello!")
        ```
        """
    )
    assert result == [
        {
            "type": "code",
            "syntax": None,
            "code": 'print("hello!")',
        }
    ]


def test_fenced_code_supports_tildes(parse_markup):
    result = parse_markup(
        """
        ~~~
        print("hello!")
        ~~~
        """
    )
    assert result == [
        {
            "type": "code",
            "syntax": None,
            "code": 'print("hello!")',
        }
    ]


def test_fenced_code_supports_syntax(parse_markup):
    result = parse_markup(
        """
        ~~~python
        print("hello!")
        ~~~
        """
    )
    assert result == [
        {
            "type": "code",
            "syntax": "python",
            "code": 'print("hello!")',
        }
    ]


def test_fenced_code_trims_syntax(parse_markup):
    result = parse_markup(
        """
        ~~~   python   
        print("hello!")
        ~~~
        """
    )
    assert result == [
        {
            "type": "code",
            "syntax": "python",
            "code": 'print("hello!")',
        }
    ]


def test_fenced_code_dedents_code(parse_markup):
    result = parse_markup(
        """
        ~~~
            def hello():
                return 1
        ~~~
        """
    )
    assert result == [
        {
            "type": "code",
            "syntax": None,
            "code": "def hello():\n    return 1",
        }
    ]


def test_fenced_code_strips_code_whitespace(parse_markup):
    result = parse_markup(
        """
        ~~~

            1 + 3

        ~~~
        """
    )
    assert result == [
        {
            "type": "code",
            "syntax": None,
            "code": "1 + 3",
        }
    ]


def test_fenced_code_can_be_mixed_with_other_blocks(parse_markup):
    result = parse_markup(
        """
        Here is the code:

        ```
        1 + 3
        ```
        It's cool!
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Here is the code:"}],
        },
        {
            "type": "code",
            "syntax": None,
            "code": "1 + 3",
        },
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "It's cool!"}],
        },
    ]


def test_fenced_code_can_be_used_next_to_each_other(parse_markup):
    result = parse_markup(
        """
        Here is the code:

        ```
        1 + 3
        ```
        ```math
        4 x 2
        ```
        It's cool!
        """
    )
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Here is the code:"}],
        },
        {
            "type": "code",
            "syntax": None,
            "code": "1 + 3",
        },
        {
            "type": "code",
            "syntax": "math",
            "code": "4 x 2",
        },
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "It's cool!"}],
        },
    ]
