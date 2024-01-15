def test_thematic_break(parse_markup):
    result = parse_markup("---")
    assert result == [
        {"type": "thematic-break"},
    ]


def test_thematic_break_with_asterisks(parse_markup):
    result = parse_markup("***")
    assert result == [
        {"type": "thematic-break"},
    ]


def test_thematic_break_with_underscores(parse_markup):
    result = parse_markup("___")
    assert result == [
        {"type": "thematic-break"},
    ]


def test_thematic_break_with_extra_signs(parse_markup):
    result = parse_markup("  -  -    -   ---    ")
    assert result == [
        {"type": "thematic-break"},
    ]


def test_thematic_break_breaks_paragraphs(parse_markup):
    result = parse_markup("Lorem ipsum\n- - -\nDolor met")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum"},
            ],
        },
        {"type": "thematic-break"},
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Dolor met"},
            ],
        },
    ]


def test_thematic_break_bbcode(parse_markup):
    result = parse_markup("[hr]")
    assert result == [
        {"type": "thematic-break-bbcode"},
    ]


def test_thematic_break_bbcode_alt(parse_markup):
    result = parse_markup("[hr/]")
    assert result == [
        {"type": "thematic-break-bbcode"},
    ]


def test_thematic_break_bbcode_breaks_paragraphs(parse_markup):
    result = parse_markup("Lorem ipsum[hr]Dolor met")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum"},
            ],
        },
        {"type": "thematic-break-bbcode"},
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Dolor met"},
            ],
        },
    ]


def test_repeated_thematic_break_is_removed(parse_markup):
    result = parse_markup("Lorem ipsum\n- - -\n[hr]Dolor met")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Lorem ipsum"},
            ],
        },
        {"type": "thematic-break"},
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Dolor met"},
            ],
        },
    ]
