def test_code_bbcode_without_args(parse_to_html):
    html = parse_to_html('[code]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_code_bbcode_with_empty_args(parse_to_html):
    html = parse_to_html('[code=]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_code_bbcode_with_blank_args(parse_to_html):
    html = parse_to_html('[code=   ]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_code_bbcode_with_empty_quoted_args(parse_to_html):
    html = parse_to_html('[code=""]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_code_bbcode_with_blank_quoted_args(parse_to_html):
    html = parse_to_html('[code="   "]\nhello("world")\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_code_bbcode_with_info_arg(parse_to_html):
    html = parse_to_html('[code=lorem]\nhello("world")\n[/code]')
    assert html == ('<misago-code info="lorem">hello(&quot;world&quot;)</misago-code>')


def test_code_bbcode_with_quoted_info_arg(parse_to_html):
    html = parse_to_html('[code="lorem"]\nhello("world")\n[/code]')
    assert html == ('<misago-code info="lorem">hello(&quot;world&quot;)</misago-code>')


def test_code_bbcode_with_syntax_arg(parse_to_html):
    html = parse_to_html('[code=php]\nhello("world")\n[/code]')
    assert html == ('<misago-code syntax="php">hello(&quot;world&quot;)</misago-code>')


def test_code_bbcode_with_quoted_syntax_arg(parse_to_html):
    html = parse_to_html('[code="php"]\nhello("world")\n[/code]')
    assert html == ('<misago-code syntax="php">hello(&quot;world&quot;)</misago-code>')


def test_code_bbcode_with_info_and_syntax_arg(parse_to_html):
    html = parse_to_html('[code=lorem; syntax=php]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code info="lorem" syntax="php">hello(&quot;world&quot;)'
        "</misago-code>"
    )


def test_code_bbcode_with_quoted_info_and_syntax_arg(parse_to_html):
    html = parse_to_html('[code="lorem; syntax=php"]\nhello("world")\n[/code]')
    assert html == (
        '<misago-code info="lorem" syntax="php">hello(&quot;world&quot;)'
        "</misago-code>"
    )


def test_code_bbcode_strips_blank_lines(parse_to_html):
    html = parse_to_html('[code]\n\n\nhello("world")\n\n\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_code_bbcode_dedents_lines(parse_to_html):
    html = parse_to_html('[code]\n    hello("world")\n\n\n[/code]')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


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


def test_code_bbcode_single_line_strips_whitespace(parse_to_html):
    html = parse_to_html('[code="lorem"]   hello("world")   [/code]')
    assert html == '<misago-code info="lorem">hello(&quot;world&quot;)</misago-code>'


def test_code_bbcode_between_paragraphs(parse_to_html):
    html = parse_to_html("paragraph1\n[code]\nhello()\n[/code]\nparagraph2")
    assert html == (
        "<p>paragraph1</p>" "\n<misago-code>hello()</misago-code>" "\n<p>paragraph2</p>"
    )


def test_code_bbcode_single_line_between_paragraphs(parse_to_html):
    html = parse_to_html("paragraph1\n[code]hello()[/code]\nparagraph2")
    assert html == (
        "<p>paragraph1</p>" "\n<misago-code>hello()</misago-code>" "\n<p>paragraph2</p>"
    )
