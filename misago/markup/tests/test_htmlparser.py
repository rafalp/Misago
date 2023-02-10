from ..htmlparser import parse_html_string, print_html_string


def test_parser_handles_simple_html():
    root_node = parse_html_string("<p>Hello World!</p>")
    assert print_html_string(root_node) == "<p>Hello World!</p>"


def test_parser_handles_html_with_brs():
    root_node = parse_html_string("<p>Hello<br />World!</p>")
    assert print_html_string(root_node) == "<p>Hello<br />World!</p>"


def test_parser_handles_html_with_hrs():
    root_node = parse_html_string("<p>Hello</p><hr /><p>World!</p>")
    assert print_html_string(root_node) == "<p>Hello</p><hr /><p>World!</p>"


def test_parser_escapes_html_in_text_nodes():
    root_node = parse_html_string("<span>Hello &lt;br&gt; World!</span>")
    assert print_html_string(root_node) == "<span>Hello &lt;br&gt; World!</span>"


def test_parser_escapes_quotes_in_text_nodes():
    root_node = parse_html_string('<span>Hello "World"!</span>')
    assert print_html_string(root_node) == "<span>Hello &quot;World&quot;!</span>"


def test_parser_handles_attributes():
    root_node = parse_html_string('<a href="/hello-world/">Hello World!</a>')
    assert print_html_string(root_node) == '<a href="/hello-world/">Hello World!</a>'


def test_parser_escapes_html_in_attributes_names():
    root_node = parse_html_string('<span data-a<tt>r="<br>">Hello!</span>')
    assert print_html_string(root_node) == (
        "<span data-a&lt;tt>r=&quot;<br />&quot;&gt;Hello!</span>"
    )


def test_parser_escapes_quotes_in_attributes_names():
    root_node = parse_html_string('<span "data-attr"="br">Hello!</span>')
    assert print_html_string(root_node) == (
        '<span &quot;data-attr&quot;="br">Hello!</span>'
    )


def test_parser_escapes_html_in_attributes_values():
    root_node = parse_html_string('<span data-attr="<br>">Hello!</span>')
    assert print_html_string(root_node) == (
        '<span data-attr="&lt;br&gt;">Hello!</span>'
    )


def test_parser_handles_escaped_attribute_values():
    root_node = parse_html_string('<span data-attr="&lt;br&gt;">Hello!</span>')
    assert print_html_string(root_node) == (
        '<span data-attr="&lt;br&gt;">Hello!</span>'
    )


def test_parser_escapes_quotes_in_attributes_values():
    root_node = parse_html_string('<span data-attr="\'">Hello!</span>')
    assert print_html_string(root_node) == ('<span data-attr="&#x27;">Hello!</span>')


def test_parser_handles_bool_attributes():
    root_node = parse_html_string("<button disabled>Hello World!</button>")
    assert print_html_string(root_node) == "<button disabled>Hello World!</button>"
