from ..parser import parse


def test_single_line_code(request_mock, user, snapshot):
    text = '[code]echo("Hello!");[/code]'
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_multi_line_code(request_mock, user, snapshot):
    text = """
[code]
echo("Hello!");

echo("World!");
[/code]
    """
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_code_with_language_parameter(request_mock, user, snapshot):
    text = '[code=php]echo("Hello!");[/code]'
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_code_with_quoted_language_parameter(request_mock, user, snapshot):
    text = '[code="php"]echo("Hello!");[/code]'
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])


def test_code_block_disables_parsing(request_mock, user, snapshot):
    text = "[code]Dolor [b]met.[/b][/code]"
    result = parse(text, request_mock, user, minify=False)
    snapshot.assert_match(result["parsed_text"])
