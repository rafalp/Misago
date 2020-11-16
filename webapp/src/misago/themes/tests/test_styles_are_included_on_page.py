from ...test import assert_contains


def test_active_theme_styles_are_included_in_page_html(client, active_theme):
    css = active_theme.css.create(name="test", url="https://cdn.example.com/style.css")
    response = client.get("/")
    assert_contains(response, 'link href="%s" rel="stylesheet"' % css.url)
