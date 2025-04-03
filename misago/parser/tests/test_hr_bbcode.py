def test_hr_bbcode(parse_to_html):
    html = parse_to_html("[hr]")
    assert html == "<hr>"


def test_hr_bbcode_before_paragraph(parse_to_html):
    html = parse_to_html("[hr]\nparagraph")
    assert html == "<hr>\n<p>paragraph</p>"


def test_hr_bbcode_after_paragraph(parse_to_html):
    html = parse_to_html("paragraph\n[hr]")
    assert html == "<p>paragraph</p>\n<hr>"


def test_hr_bbcode_between_paragraphs(parse_to_html):
    html = parse_to_html("paragraph1\n[hr]\nparagraph2")
    assert html == "<p>paragraph1</p>\n<hr>\n<p>paragraph2</p>"


def test_hr_bbcode_repeated_in_line(parse_to_html):
    html = parse_to_html("paragraph1\n[hr]  [hr]  [hr]  [hr]\nparagraph2")
    assert html == "<p>paragraph1</p>\n<hr>\n<p>paragraph2</p>"


def test_hr_bbcode_repeated_in_separate_lines(parse_to_html):
    html = parse_to_html("paragraph1\n[hr]\n[hr]\n\n[hr]\n[hr]\nparagraph2")
    assert html == "<p>paragraph1</p>\n<hr>\n<p>paragraph2</p>"


def test_hr_bbcode_after_markdown_hr(parse_to_html):
    html = parse_to_html("paragraph1\n- - -\n[hr]\nparagraph2")
    assert html == "<p>paragraph1</p>\n<hr>\n<p>paragraph2</p>"
