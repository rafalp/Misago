def test_markdown_table_has_css_styles_set(parse_to_html):
    html = parse_to_html("| table |\n| --- |\n| cell |")
    assert html.startswith('<table class="rich-text-table">')
