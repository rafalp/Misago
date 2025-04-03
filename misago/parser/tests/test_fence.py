def test_fenced_code_without_params(parse_to_html):
    html = parse_to_html('```\nhello("world")')
    assert html == "<misago-code>hello(&quot;world&quot;)</misago-code>"


def test_fence_code_with_info_param(parse_to_html):
    html = parse_to_html('```lorem\nhello("world")')
    assert html == ('<misago-code info="lorem">hello(&quot;world&quot;)</misago-code>')


def test_fence_code_with_syntax_param(parse_to_html):
    html = parse_to_html('```php\nhello("world")')
    assert html == ('<misago-code syntax="php">hello(&quot;world&quot;)</misago-code>')


def test_fence_code_with_info_and_syntax_param(parse_to_html):
    html = parse_to_html('```lorem; syntax=php\nhello("world")')
    assert html == (
        '<misago-code info="lorem" syntax="php">hello(&quot;world&quot;)'
        "</misago-code>"
    )
