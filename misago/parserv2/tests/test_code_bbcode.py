def test_code_bbcode_without_args(parse_to_html):
    html = parse_to_html('[code]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)\n</misago-code>"


def test_code_bbcode_with_empty_args(parse_to_html):
    html = parse_to_html('[code=]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)\n</misago-code>"


def test_code_bbcode_with_blank_args(parse_to_html):
    html = parse_to_html('[code=   ]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)\n</misago-code>"


def test_code_bbcode_with_empty_quoted_args(parse_to_html):
    html = parse_to_html('[code=""]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)\n</misago-code>"


def test_code_bbcode_with_blank_quoted_args(parse_to_html):
    html = parse_to_html('[code="   "]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)\n</misago-code>"


def test_code_bbcode_with_info_arg(parse_to_html):
    html = parse_to_html('[code=lorem]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code info="lorem">hello(&quot;world&quot;)\n</misago-code>'
    )


def test_code_bbcode_with_quoted_info_arg(parse_to_html):
    html = parse_to_html('[code="lorem"]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code info="lorem">hello(&quot;world&quot;)\n</misago-code>'
    )


def test_code_bbcode_with_syntax_arg(parse_to_html):
    html = parse_to_html('[code=php]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code syntax="php">hello(&quot;world&quot;)\n</misago-code>'
    )


def test_code_bbcode_with_quoted_syntax_arg(parse_to_html):
    html = parse_to_html('[code="php"]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code syntax="php">hello(&quot;world&quot;)\n</misago-code>'
    )


def test_code_bbcode_with_info_and_syntax_arg(parse_to_html):
    html = parse_to_html('[code=lorem; syntax=php]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code info="lorem" syntax="php">hello(&quot;world&quot;)\n'
        "</misago-code>"
    )


def test_code_bbcode_with_quoted_info_and_syntax_arg(parse_to_html):
    html = parse_to_html('[code="lorem; syntax=php"]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code info="lorem" syntax="php">hello(&quot;world&quot;)\n'
        "</misago-code>"
    )


def test_code_bbcode_without_args_single_line(parse_to_html):
    html = parse_to_html('[code]hello("world")[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_code_bbcode_with_syntax_arg_single_line(parse_to_html):
    html = parse_to_html('[code=php]hello("world")[/code]')
    assert html == '<misago-code syntax="php">hello(&quot;world&quot;)</misago-code>'


def test_code_bbcode_with_info_arg_single_line(parse_to_html):
    html = parse_to_html('[code=lorem]hello("world")[/code]')
    assert html == '<misago-code info="lorem">hello(&quot;world&quot;)</misago-code>'


def test_code_bbcode_with_quoted_arg_single_line(parse_to_html):
    html = parse_to_html('[code="lorem"]hello("world")[/code]')
    assert html == '<misago-code info="lorem">hello(&quot;world&quot;)</misago-code>'
