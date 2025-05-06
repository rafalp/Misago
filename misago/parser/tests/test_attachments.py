def test_attachment(parse_to_html):
    html = parse_to_html("<attachment=image.png:12>")
    assert html == (
        '<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
    )


def test_multiple_attachments_in_one_line(parse_to_html):
    html = parse_to_html("<attachment=image.png:12><attachment=text.png:13>")
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
        "\n<p>** Dolor met</p>"
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


def test_attachments_with_softbreak_spaces_between(parse_to_html):
    html = parse_to_html("<attachment=image.png:12>\n   \n<attachment=text.png:13>")
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


def test_attachment_in_blockquote(parse_to_html):
    html = parse_to_html("> <attachment=image.png:12>")
    assert html == (
        "<misago-quote>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n</misago-quote>"
    )


def test_attachment_in_single_line_quote(parse_to_html):
    html = parse_to_html("[quote]<attachment=image.png:12>[/quote]")
    assert html == (
        "<misago-quote>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n</misago-quote>"
    )


def test_attachment_in_table_cell(parse_to_html):
    html = parse_to_html(
        "| file | upload |" "\n| - | - |" "\n| image | <attachment=image.png:12> |"
    )
    assert html == (
        '<div class="rich-text-table-container">'
        '\n<table class="rich-text-table">'
        "\n<thead>"
        "\n<tr>"
        '\n<th misago-table-col="0:c">file</th>'
        '\n<th misago-table-col="1:c">upload</th>'
        "\n</tr>"
        "\n</thead>"
        "\n<tbody>"
        "\n<tr>"
        '\n<td misago-table-col="0:c">image</td>'
        '\n<td misago-table-col="1:c">'
        '<misago-attachment name="image.png" slug="image-png" id="12">'
        '</td>'
        "\n</tr>"
        "\n</tbody>"
        "\n</table>"
        "\n</div>"
    )


def test_attachment_in_list_item(parse_to_html):
    html = parse_to_html("1. <attachment=image.png:12>")
    assert html == (
        '<ol class="rich-text-list-loose">'
        "\n<li>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n</li>"
        "\n</ol>"
    )


def test_attachment_breaks_list_item(parse_to_html):
    html = parse_to_html("1. Lorem <attachment=image.png:12> ipsum")
    assert html == (
        '<ol class="rich-text-list-loose">'
        "\n<li>"
        "\n<p>Lorem</p>"
        '\n<div class="rich-text-attachment-group">'
        '\n<misago-attachment name="image.png" slug="image-png" id="12">'
        "\n</div>"
        "\n<p>ipsum</p>"
        "\n</li>"
        "\n</ol>"
    )
