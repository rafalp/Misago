from ..htmlelement import html_element


def test_html_element_returns_single_tag():
    assert html_element("hr") == "<hr />"


def test_html_element_returns_single_tag_with_bool_attribute():
    html = html_element("hr", attrs={"misago-data": True})
    assert html == "<hr misago-data />"


def test_html_element_returns_single_tag_with_str_attribute():
    html = html_element("img", attrs={"src": "https://example.com"})
    assert html == '<img src="https://example.com" />'


def test_html_element_returns_single_tag_with_empty_alt_attribute():
    html = html_element("img", attrs={"alt": ""})
    assert html == '<img alt="" />'


def test_html_element_returns_tag_with_content():
    html = html_element("b", "string")
    assert html == "<b>string</b>"


def test_html_element_returns_tag_with_empty_content():
    html = html_element("b", "")
    assert html == "<b></b>"


def test_html_element_returns_tag_with_content_and_attributes():
    html = html_element("b", "string", {"class": "text-muted", "misago-data": True})
    assert html == '<b class="text-muted" misago-data>string</b>'
