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


def test_attachments_with_paragraph_between(parse_to_html):
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
