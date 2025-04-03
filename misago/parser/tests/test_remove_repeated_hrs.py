def test_markdown_hr_after_markdown_hr_is_removed(parse_to_html):
    html = parse_to_html("- - -\n* * *")
    assert html.startswith("<hr>")


def test_markdown_hr_after_bbcode_hr_is_removed(parse_to_html):
    html = parse_to_html("[hr]\n- - -")
    assert html.startswith("<hr>")


def test_bbcode_hr_after_markdown_hr_is_removed(parse_to_html):
    html = parse_to_html("- - -\n[hr]")
    assert html.startswith("<hr>")
