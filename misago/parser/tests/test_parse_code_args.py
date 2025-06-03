from ..codeargs import parse_code_args


def test_parse_code_args_returns_none_for_empty_str():
    args = parse_code_args("")
    assert args is None


def test_parse_code_args_returns_info_for_custom_str():
    args = parse_code_args("lorem ipsum")
    assert args == {"info": "lorem ipsum"}


def test_parse_code_args_returns_unescaped_info_for_custom_str():
    args = parse_code_args("lorem ipsum\\!")
    assert args == {"info": "lorem ipsum!"}


def test_parse_code_args_returns_syntax_for_pygments_syntax_str():
    args = parse_code_args("Python")
    assert args == {"syntax": "python"}


def test_parse_code_args_returns_syntax_from_prefix_str():
    args = parse_code_args("syntax: php")
    assert args == {"syntax": "php"}


def test_parse_code_args_returns_syntax_from_escaped_prefix_str():
    args = parse_code_args("syntax: php\\!")
    assert args == {"syntax": "php!"}


def test_parse_code_args_returns_none_for_empty_syntax():
    args = parse_code_args("syntax:")
    assert args is None


def test_parse_code_args_returns_info_and_syntax():
    args = parse_code_args("lorem ipsum ; syntax: php")
    assert args == {"info": "lorem ipsum", "syntax": "php"}


def test_parse_code_args_returns_unescaped_info_and_syntax():
    args = parse_code_args("lorem ipsum \\; syntax\\: php")
    assert args == {"info": "lorem ipsum ; syntax: php"}


def test_parse_code_args_returns_unescaped_info_and_unescaped_syntax():
    args = parse_code_args("lorem\\!ipsum ; syntax: php\\!")
    assert args == {"info": "lorem!ipsum", "syntax": "php!"}
