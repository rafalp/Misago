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
