def test_attachment(parse_to_html):
    html = parse_to_html("<attachment=image.png:12>")
    assert html == (
        '<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
    )


def test_multiple_attachments_in_one_line(parse_to_html):
    html = parse_to_html("<attachment=image.png:12> <attachment=text.png:13>")
    assert html == (
        '<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        '\n<misago-attachment name="text.png" slug="text-png" id="13">'
        "\n</div>"
    )


def test_attachment_breaks_paragraph(parse_to_html):
    html = parse_to_html("Lorem ipsum <attachment=image.png:12> Dolor met")
    assert html == (
        "<p>Lorem ipsum</p>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n<p>Dolor met</p>"
    )


def test_attachment_breaks_inline_markdown(parse_to_html):
    html = parse_to_html("Lorem ipsum **<attachment=image.png:12>** Dolor met")
    assert html == (
        "<p>Lorem ipsum **</p>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n<p>* Dolor met</p>"
    )


def test_attachment_breaks_inline_bbcode(parse_to_html):
    html = parse_to_html("Lorem ipsum [b]<attachment=image.png:12>[/b] Dolor met")
    assert html == (
        "<p>Lorem ipsum [b]</p>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n<p>[/b] Dolor met</p>"
    )


def test_attachments_with_paragraph_text_between(parse_to_html):
    html = parse_to_html(
        "<attachment=image.png:12> Lorem ipsum <attachment=text.png:13>"
    )
    assert html == (
        '<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n<p>Lorem ipsum</p>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="text.png" slug="text-png" id="13">'
        "\n</div>"
    )


def test_attachments_with_paragraph_spaces_between(parse_to_html):
    html = parse_to_html("<attachment=image.png:12>   <attachment=text.png:13>")
    assert html == (
        '<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        '\n<misago-attachment name="text.png" slug="text-png" id="13">'
        "\n</div>"
    )


def test_attachments_with_softbreak_between(parse_to_html):
    html = parse_to_html("<attachment=image.png:12>\n<attachment=text.png:13>")
    assert html == (
        '<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        '\n<misago-attachment name="text.png" slug="text-png" id="13">'
        "\n</div>"
    )


def test_attachments_with_hardbreak_between(parse_to_html):
    html = parse_to_html("<attachment=image.png:12>\n\n\n<attachment=text.png:13>")
    assert html == (
        '<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        '\n<misago-attachment name="text.png" slug="text-png" id="13">'
        "\n</div>"
    )
