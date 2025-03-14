from ..replace import (
    replace_html_element,
    replace_html_element_func,
    replace_html_void_element,
    replace_html_void_element_func,
)


def test_replace_html_element_replaces_single_element():
    def replace_p(match) -> str:
        return f"<div>{match.group('children')}</div>"

    document = "<p>element children</p>"
    result = replace_html_element(document, "p", replace_p)
    assert result == "<div>element children</div>"


def test_replace_html_element_replaces_multiple_elements():
    def replace_p(match) -> str:
        return f"<div>{match.group('children')}</div>"

    document = "<p>first</p> <p>second</p>"
    result = replace_html_element(document, "p", replace_p)
    assert result == "<div>first</div> <div>second</div>"


def test_replace_html_element_replaces_element_with_args():
    @replace_html_element_func
    def replace_div(html: str, children: str, args: dict | None = None) -> str:
        assert args == {"arg": "oh wow", "data-arg": "wop", "bool": True}
        return f"<p>{children}</p>"

    document = '<div arg="oh wow" data-arg="wop" bool>first</div>'
    result = replace_html_element(document, "div", replace_div)
    assert result == "<p>first</p>"


def test_replace_void_html_element_replaces_single_element():
    def replace_p(match) -> str:
        return f"<div></div>"

    document = "<hr>"
    result = replace_html_void_element(document, "hr", replace_p)
    assert result == "<div></div>"


def test_replace_void_html_element_replaces_single_element_with_slash():
    def replace_p(match) -> str:
        return f"<div></div>"

    document = "<hr />"
    result = replace_html_void_element(document, "hr", replace_p)
    assert result == "<div></div>"


def test_replace_void_html_element_replaces_multiple_elements():
    def replace_p(match) -> str:
        return f"<div>{match.group(0)}</div>"

    document = "<hr> <hr />"
    result = replace_html_void_element(document, "hr", replace_p)
    assert result == "<div><hr></div> <div><hr /></div>"


def test_replace_void_html_element_replaces_element_with_args():
    @replace_html_void_element_func
    def replace_div(html: str, args: dict | None = None) -> str:
        assert args == {"arg": "oh wow", "data-arg": "wop", "bool": True}
        return f"<p>{html}</p>"

    document = '<hr arg="oh wow" data-arg="wop" bool />'
    result = replace_html_void_element(document, "hr", replace_div)
    assert result == '<p><hr arg="oh wow" data-arg="wop" bool /></p>'
