def test_spoiler_bbcode(parse_markup):
    result = parse_markup("[spoiler]Hello world![/spoiler]")
    assert result == [
        {
            "type": "spoiler-bbcode",
            "summary": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_spoiler_bbcode_with_empty_summary(parse_markup):
    result = parse_markup("[spoiler=]Hello world![/spoiler]")
    assert result == [
        {
            "type": "spoiler-bbcode",
            "summary": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_spoiler_bbcode_with_summary(parse_markup):
    result = parse_markup("[spoiler=Dune, part 2]Hello world![/spoiler]")
    assert result == [
        {
            "type": "spoiler-bbcode",
            "summary": "Dune, part 2",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_spoiler_bbcode_strips_quotations_and_spaces_from_summary(parse_markup):
    result = parse_markup('[spoiler="  Dune, part 2 "]Hello world![/spoiler]')
    assert result == [
        {
            "type": "spoiler-bbcode",
            "summary": "Dune, part 2",
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Hello world!"}],
                },
            ],
        },
    ]


def test_empty_spoiler_bbcode_is_removed_from_result(parse_markup):
    result = parse_markup("Lorem ipsum.[spoiler][/spoiler]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
    ]


def test_blank_spoiler_bbcode_is_removed_from_result(parse_markup):
    result = parse_markup("Lorem ipsum.[spoiler]   [/spoiler]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
    ]


def test_spoiler_bbcode_next_to_paragraph_is_parsed(parse_markup):
    result = parse_markup("Lorem ipsum.[spoiler]Dolor met![/spoiler]")
    assert result == [
        {
            "type": "paragraph",
            "children": [{"type": "text", "text": "Lorem ipsum."}],
        },
        {
            "type": "spoiler-bbcode",
            "summary": None,
            "children": [
                {
                    "type": "paragraph",
                    "children": [{"type": "text", "text": "Dolor met!"}],
                },
            ],
        },
    ]
