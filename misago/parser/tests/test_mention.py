def test_mention(parse_markup):
    result = parse_markup("Hello @Bob_Boberston!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "mention",
                    "username": "Bob_Boberston",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]


def test_mention_unescapes_username(parse_markup):
    result = parse_markup("Hello @Bob\_Boberston!")
    assert result == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello "},
                {
                    "type": "mention",
                    "username": "Bob_Boberston",
                },
                {"type": "text", "text": "!"},
            ],
        }
    ]
