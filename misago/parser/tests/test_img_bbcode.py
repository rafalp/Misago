def test_img_bbcode(parse_to_html):
    html = parse_to_html("[img]example.com[/img]")
    assert html == '<p><img src="example.com" alt=""></p>'


def test_img_bbcode_without_content(parse_to_html):
    html = parse_to_html("[img][/img]")
    assert html == "<p>[img][/img]</p>"


def test_img_bbcode_with_blank_content(parse_to_html):
    html = parse_to_html("[img]   [/img]")
    assert html == "<p>[img]   [/img]</p>"


def test_img_bbcode_with_invalid_img(parse_to_html):
    html = parse_to_html("[img]invalid[/img]")
    assert html == '<p><img src="invalid" alt=""></p>'


def test_img_bbcode_with_arg(parse_to_html):
    html = parse_to_html("[img=example.com]Hello[/img]")
    assert html == '<p><img src="example.com" alt="Hello"></p>'


def test_img_bbcode_with_empty_arg(parse_to_html):
    html = parse_to_html("[img=]Hello[/img]")
    assert html == "<p>[img=]Hello[/img]</p>"


def test_img_bbcode_with_blank_arg(parse_to_html):
    html = parse_to_html("[img=   ]Hello[/img]")
    assert html == "<p>[img=   ]Hello[/img]</p>"


def test_img_bbcode_with_quoted_arg(parse_to_html):
    html = parse_to_html('[img="example.com"]Hello[/img]')
    assert html == '<p><img src="example.com" alt="Hello"></p>'


def test_img_bbcode_with_invalid_arg(parse_to_html):
    html = parse_to_html("[img=invalid]Hello[/img]")
    assert html == '<p><img src="invalid" alt="Hello"></p>'
