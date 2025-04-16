def test_tight_ordered_list_items_have_tight_flag(parse_to_tokens):
    for token in parse_to_tokens("1. Tight list"):
        if token.type in ("ordered_list_open", "list_item_open"):
            assert token.meta["tight"]


def test_tight_ordered_list_has_css_class(parse_to_html):
    html = parse_to_html("1. Tight list")
    assert html == (
        '<ol class="rich-text-list-tight">' "\n<li>Tight list</li>" "\n</ol>"
    )


def test_loose_ordered_list_items_have_tight_flag(parse_to_tokens):
    for token in parse_to_tokens("1. First line\n\n   Second line"):
        if token.type in ("ordered_list_open", "list_item_open"):
            assert not token.meta["tight"]


def test_loose_ordered_list_has_css_class(parse_to_html):
    html = parse_to_html("1. First line\n\n   Second line\n2. Next item")
    assert html == (
        '<ol class="rich-text-list-loose">'
        "\n<li>"
        "\n<p>First line</p>"
        "\n<p>Second line</p>"
        "\n</li>"
        "\n<li>"
        "\n<p>Next item</p>"
        "\n</li>"
        "\n</ol>"
    )


def test_tight_bullet_list_items_have_tight_flag(parse_to_tokens):
    for token in parse_to_tokens("- Tight list"):
        if token.type in ("bullet_list_open", "list_item_open"):
            assert token.meta["tight"]


def test_tight_bullet_list_has_css_class(parse_to_html):
    html = parse_to_html("- Tight list")
    assert html == (
        '<ul class="rich-text-list-tight">' "\n<li>Tight list</li>" "\n</ul>"
    )


def test_loose_bullet_list_items_have_tight_flag(parse_to_tokens):
    for token in parse_to_tokens("- First line\n\n  Second line"):
        if token.type in ("bullet_list_open", "list_item_open"):
            assert not token.meta["tight"]


def test_loose_bullet_list_has_css_class(parse_to_html):
    html = parse_to_html("- First line\n\n  Second line\n- Next item")
    assert html == (
        '<ul class="rich-text-list-loose">'
        "\n<li>"
        "\n<p>First line</p>"
        "\n<p>Second line</p>"
        "\n</li>"
        "\n<li>"
        "\n<p>Next item</p>"
        "\n</li>"
        "\n</ul>"
    )
