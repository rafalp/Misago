def test_youtube_link(parse_to_html):
    html = parse_to_html("https://www.youtube.com/watch?v=QzfXag4r7Vo")
    assert html == (
        "<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
    )


def test_multiple_youtube_links_in_one_line(parse_to_html):
    html = parse_to_html(
        "https://www.youtube.com/watch?v=QzfXag4r7Vo "
        "https://www.youtube.com/watch?v=4YEbVHtofys"
    )
    assert html == (
        "<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n"
        "<misago-video "
        'href="https://www.youtube.com/watch?v=4YEbVHtofys" '
        'site="youtube" '
        'video="4YEbVHtofys"'
        ">"
    )


def test_youtube_link_doesnt_break_paragraph(parse_to_html):
    html = parse_to_html(
        "Lorem ipsum https://www.youtube.com/watch?v=QzfXag4r7Vo Dolor met"
    )
    assert html == (
        "<p>Lorem ipsum "
        "<a "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "www.youtube.com/watch?v=QzfXag4r7Vo"
        "</a>"
        " Dolor met</p>"
    )


def test_youtube_link_doesnt_break_inline_markdown(parse_to_html):
    html = parse_to_html(
        "Lorem ipsum **https://www.youtube.com/watch?v=QzfXag4r7Vo** Dolor met"
    )
    assert html == (
        "<p>Lorem ipsum "
        "<strong>"
        "<a "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "www.youtube.com/watch?v=QzfXag4r7Vo"
        "</a>"
        "</strong>"
        " Dolor met</p>"
    )


def test_youtube_link_doesnt_break_inline_bbcode(parse_to_html):
    html = parse_to_html(
        "Lorem ipsum [b]https://www.youtube.com/watch?v=QzfXag4r7Vo[/b] Dolor met"
    )
    assert html == (
        "<p>Lorem ipsum "
        "<b>"
        "<a "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "www.youtube.com/watch?v=QzfXag4r7Vo"
        "</a>"
        "</b>"
        " Dolor met</p>"
    )


def test_youtube_link_with_paragraph_text_around(parse_to_html):
    html = parse_to_html(
        "Lorem ipsum" "\nhttps://www.youtube.com/watch?v=QzfXag4r7Vo" "\nDolor met"
    )
    assert html == (
        "<p>Lorem ipsum</p>"
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n<p>Dolor met</p>"
    )


def test_youtube_links_with_paragraph_text_between(parse_to_html):
    html = parse_to_html(
        "https://www.youtube.com/watch?v=QzfXag4r7Vo"
        " Lorem ipsum "
        "https://www.youtube.com/watch?v=4YEbVHtofys"
    )
    assert html == (
        "<p>"
        "<a "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "www.youtube.com/watch?v=QzfXag4r7Vo"
        "</a>"
        " Lorem ipsum "
        "<a "
        'href="https://www.youtube.com/watch?v=4YEbVHtofys" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "www.youtube.com/watch?v=4YEbVHtofys"
        "</a>"
        "</p>"
    )


def test_youtube_links_with_paragraph_spaces_between(parse_to_html):
    html = parse_to_html(
        "https://www.youtube.com/watch?v=QzfXag4r7Vo"
        "   "
        "https://www.youtube.com/watch?v=4YEbVHtofys"
    )
    assert html == (
        "<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=4YEbVHtofys" '
        'site="youtube" '
        'video="4YEbVHtofys"'
        ">"
    )


def test_youtube_links_with_softbreak_between(parse_to_html):
    html = parse_to_html(
        "https://www.youtube.com/watch?v=QzfXag4r7Vo"
        "\n"
        "https://www.youtube.com/watch?v=4YEbVHtofys"
    )
    assert html == (
        "<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=4YEbVHtofys" '
        'site="youtube" '
        'video="4YEbVHtofys"'
        ">"
    )


def test_youtube_links_with_softbreak_spaces_between(parse_to_html):
    html = parse_to_html(
        "https://www.youtube.com/watch?v=QzfXag4r7Vo"
        "\n   \n"
        "https://www.youtube.com/watch?v=4YEbVHtofys"
    )
    assert html == (
        "<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=4YEbVHtofys" '
        'site="youtube" '
        'video="4YEbVHtofys"'
        ">"
    )


def test_youtube_links_with_hardbreak_between(parse_to_html):
    html = parse_to_html(
        "https://www.youtube.com/watch?v=QzfXag4r7Vo"
        "\n\n\n"
        "https://www.youtube.com/watch?v=4YEbVHtofys"
    )
    assert html == (
        "<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=4YEbVHtofys" '
        'site="youtube" '
        'video="4YEbVHtofys"'
        ">"
    )


def test_youtube_link_in_blockquote(parse_to_html):
    html = parse_to_html("> https://www.youtube.com/watch?v=QzfXag4r7Vo")
    assert html == (
        "<misago-quote>"
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n</misago-quote>"
    )


def test_youtube_link_in_single_line_quote(parse_to_html):
    html = parse_to_html("[quote]https://www.youtube.com/watch?v=QzfXag4r7Vo[/quote]")
    assert html == (
        "<misago-quote>"
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n</misago-quote>"
    )


def test_youtube_link_alone_in_table_cell(parse_to_html):
    html = parse_to_html(
        "| file | upload |"
        "\n| - | - |"
        "\n| image | https://www.youtube.com/watch?v=QzfXag4r7Vo |"
    )
    assert html == (
        '<div class="rich-text-table-container" misago-rich-text="table-container">'
        '\n<table class="rich-text-table">'
        "\n<thead>"
        '\n<tr id="misago-table-tr-random1">'
        '\n<th misago-rich-text-col="0:c">file</th>'
        '\n<th misago-rich-text-col="1:c">upload</th>'
        "\n</tr>"
        "\n</thead>"
        "\n<tbody>"
        '\n<tr id="misago-table-tr-random2">'
        '\n<td misago-rich-text-col="0:c">image</td>'
        '\n<td misago-rich-text-col="1:c">'
        "\n<misago-video "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'site="youtube" '
        'video="QzfXag4r7Vo"'
        ">"
        "\n</td>"
        "\n</tr>"
        "\n</tbody>"
        "\n</table>"
        "\n</div>"
    )


def test_youtube_link_with_text_in_table_cell(parse_to_html):
    html = parse_to_html(
        "| file | upload |"
        "\n| - | - |"
        "\n| image | link: https://www.youtube.com/watch?v=QzfXag4r7Vo |"
    )
    assert html == (
        '<div class="rich-text-table-container" misago-rich-text="table-container">'
        '\n<table class="rich-text-table">'
        "\n<thead>"
        '\n<tr id="misago-table-tr-random1">'
        '\n<th misago-rich-text-col="0:c">file</th>'
        '\n<th misago-rich-text-col="1:c">upload</th>'
        "\n</tr>"
        "\n</thead>"
        "\n<tbody>"
        '\n<tr id="misago-table-tr-random2">'
        '\n<td misago-rich-text-col="0:c">image</td>'
        '\n<td misago-rich-text-col="1:c">'
        "link: "
        "<a "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">www.youtube.com/watch?v=QzfXag4r7Vo</a>"
        "</td>"
        "\n</tr>"
        "\n</tbody>"
        "\n</table>"
        "\n</div>"
    )


def test_youtube_link_in_list_item(parse_to_html):
    html = parse_to_html("1. https://www.youtube.com/watch?v=QzfXag4r7Vo")
    assert html == (
        '<ol class="rich-text-list-tight">'
        "\n<li>"
        "<a "
        'href="https://www.youtube.com/watch?v=QzfXag4r7Vo" '
        'rel="external nofollow noopener" '
        'target="_blank" '
        'misago-rich-text="autolink"'
        ">"
        "www.youtube.com/watch?v=QzfXag4r7Vo</a>"
        "</li>"
        "\n</ol>"
    )
