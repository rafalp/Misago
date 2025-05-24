def test_markdown_table_has_responsive_container(parse_to_html):
    html = parse_to_html("| table |\n| --- |\n| cell |").strip()
    assert html.startswith(
        '<div class="rich-text-table-container" misago-rich-text="table-container">'
    )
    assert html.endswith("</div>")


def test_markdown_table_has_css_styles_set(parse_to_html):
    html = parse_to_html("| table |\n| --- |\n| cell |")
    assert '<table class="rich-text-table">' in html
    assert "<table>" not in html
