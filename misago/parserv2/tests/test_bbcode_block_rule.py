def test_bbcode_block_rule_parses_single_line_block(parse_to_html):
    html = parse_to_html("[quote]text[/quote]")
    assert html == "<misago-quote>\n<p>text</p>\n</misago-quote>"


def test_bbcode_block_rule_parses_single_line_block_after_paragraph(parse_to_html):
    html = parse_to_html("paragraph\n[quote]text[/quote]")
    assert html == "<p>paragraph</p>\n<misago-quote>\n<p>text</p>\n</misago-quote>"


def test_bbcode_block_rule_parses_single_line_block_before_paragraph(parse_to_html):
    html = parse_to_html("[quote]text[/quote]\nparagraph")
    assert html == "<misago-quote>\n<p>text</p>\n</misago-quote>\n<p>paragraph</p>"


def test_bbcode_block_rule_parses_single_line_block_between_paragraphs(parse_to_html):
    html = parse_to_html("paragraph1\n[quote]text[/quote]\nparagraph2")
    assert html == (
        "<p>paragraph1</p>"
        "\n<misago-quote>\n<p>text</p>\n</misago-quote>"
        "\n<p>paragraph2</p>"
    )


def test_bbcode_block_rule_parses_single_line_block_contents(parse_to_html):
    html = parse_to_html("[quote]lorem **ipsum** dolor[/quote]")
    assert html == (
        "<misago-quote>\n<p>lorem <strong>ipsum</strong> dolor</p>\n</misago-quote>"
    )


def test_bbcode_block_rule_parses_multiline_block(parse_to_html):
    html = parse_to_html("[quote]\ntext\n[/quote]")
    assert html == "<misago-quote>\n<p>text</p>\n</misago-quote>"


def test_bbcode_block_rule_parses_multiline_block_contents(parse_to_html):
    html = parse_to_html("[quote]\nlorem **ipsum** dolor\n[/quote]")
    assert html == (
        "<misago-quote>\n<p>lorem <strong>ipsum</strong> dolor</p>\n</misago-quote>"
    )


def test_bbcode_block_rule_parses_multiline_block_after_paragraph(parse_to_html):
    html = parse_to_html("paragraph\n[quote]\ntext\n[/quote]")
    assert html == "<p>paragraph</p>\n<misago-quote>\n<p>text</p>\n</misago-quote>"


def test_bbcode_block_rule_parses_multiline_block_before_paragraph(parse_to_html):
    html = parse_to_html("[quote]\ntext\n[/quote]\nparagraph")
    assert html == "<misago-quote>\n<p>text</p>\n</misago-quote>\n<p>paragraph</p>"


def test_bbcode_block_rule_parses_multiline_block_between_paragraphs(parse_to_html):
    html = parse_to_html("paragraph1\n[quote]\ntext\n[/quote]\nparagraph2")
    assert html == (
        "<p>paragraph1</p>"
        "\n<misago-quote>\n<p>text</p>\n</misago-quote>"
        "\n<p>paragraph2</p>"
    )


def test_bbcode_block_rule_parses_single_line_block_in_multiline_block(parse_to_html):
    html = parse_to_html("[quote]\n[quote]nested[/quote]\n[/quote]")
    assert html == (
        "<misago-quote>"
        "\n<misago-quote>"
        "\n<p>nested</p>"
        "\n</misago-quote>"
        "\n</misago-quote>"
    )


def test_bbcode_block_rule_matches_closest_multiline_block_open_close_pair(
    parse_to_html,
):
    html = parse_to_html("[quote]\n[quote]\ntext\n[/quote]")
    assert html == (
        "<p>[quote]</p>" "\n<misago-quote>" "\n<p>text</p>" "\n</misago-quote>"
    )
