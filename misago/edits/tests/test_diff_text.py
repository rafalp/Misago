from ..diff import diff_text


def test_diff_text_diffs_same_content():
    result = diff_text("Lorem ipsum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": None,
            "text": "Lorem ipsum",
        },
    ]
    assert result.added == 0
    assert result.removed == 0


def test_diff_text_diffs_different_content():
    result = diff_text("Lorem ipsum", "Dolor met")
    assert result.lines == [
        {
            "marker": "-",
            "text": "Lorem ipsum",
        },
        {
            "marker": "+",
            "text": "Dolor met",
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_removed_character():
    result = diff_text("Lorem ipsuum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": None,
                    "text": "Lorem ipsu",
                    "length": 10,
                },
                {
                    "index": 10,
                    "marker": "-",
                    "text": "u",
                    "length": 1,
                },
                {
                    "index": 11,
                    "marker": None,
                    "text": "m",
                    "length": 1,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_added_character():
    result = diff_text("Lorem ipum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": None,
                    "text": "Lorem ip",
                    "length": 8,
                },
                {
                    "index": 8,
                    "marker": "+",
                    "text": "s",
                    "length": 1,
                },
                {
                    "index": 9,
                    "marker": None,
                    "text": "um",
                    "length": 2,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_changed_character():
    result = diff_text("Lorem iplum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": None,
                    "text": "Lorem ip",
                    "length": 8,
                },
                {
                    "index": 8,
                    "marker": "-",
                    "text": "l",
                    "length": 1,
                },
                {
                    "index": 8,
                    "marker": "+",
                    "text": "s",
                    "length": 1,
                },
                {
                    "index": 9,
                    "marker": None,
                    "text": "um",
                    "length": 2,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_changed_some_character():
    result = diff_text("Lorem islum", "Lolem iplum")
    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": None,
                    "text": "Lo",
                    "length": 2,
                },
                {
                    "index": 2,
                    "marker": "-",
                    "text": "r",
                    "length": 1,
                },
                {
                    "index": 2,
                    "marker": "+",
                    "text": "l",
                    "length": 1,
                },
                {
                    "index": 3,
                    "marker": None,
                    "text": "em i",
                    "length": 4,
                },
                {
                    "index": 7,
                    "marker": "-",
                    "text": "s",
                    "length": 1,
                },
                {
                    "index": 7,
                    "marker": "+",
                    "text": "p",
                    "length": 1,
                },
                {
                    "index": 8,
                    "marker": None,
                    "text": "lum",
                    "length": 3,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_real_case_1():
    result = diff_text(
        "Basically, start from there: https://misago.gitbook.io/docs/setup/misago#downloading-misago-on-the-server",
        "If you want to go the `misago-docker` route, start from there: https://misago.gitbook.io/docs/setup/misago#downloading-misago-on-the-server",
    )

    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": "-",
                    "text": "Basically",
                    "length": 9,
                },
                {
                    "index": 0,
                    "marker": "+",
                    "text": "If you want to go the `misago-docker` route",
                    "length": 43,
                },
                {
                    "index": 43,
                    "marker": None,
                    "text": ", start from there: https://misago.gitbook.io/docs/setup/misago#downloading-misago-on-the-server",
                    "length": 96,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_real_case_2():
    result = diff_text(
        "UI for private thread members",
        "Manage private threads members",
    )

    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": "-",
                    "text": "UI for",
                    "length": 6,
                },
                {
                    "index": 0,
                    "marker": "+",
                    "text": "Manage",
                    "length": 6,
                },
                {
                    "index": 6,
                    "marker": None,
                    "text": " private thread",
                    "length": 15,
                },
                {
                    "index": 21,
                    "marker": "+",
                    "text": "s",
                    "length": 1,
                },
                {
                    "index": 22,
                    "marker": None,
                    "text": " members",
                    "length": 8,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_real_case_3():
    result = diff_text(
        "User signatures",
        "Add user signatures",
    )

    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": "-",
                    "text": "U",
                    "length": 1,
                },
                {
                    "index": 0,
                    "marker": "+",
                    "text": "Add u",
                    "length": 5,
                },
                {
                    "index": 5,
                    "marker": None,
                    "text": "ser signatures",
                    "length": 14,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_real_case_4():
    result = diff_text(
        "Metatags for search engines and social sites",
        "Add metatags for search engines and social sites to pages missing them",
    )

    assert result.lines == [
        {
            "marker": "?",
            "diff": [
                {
                    "index": 0,
                    "marker": "-",
                    "text": "M",
                    "length": 1,
                },
                {
                    "index": 0,
                    "marker": "+",
                    "text": "Add m",
                    "length": 5,
                },
                {
                    "index": 5,
                    "marker": None,
                    "text": "etatags for search engines and social sites",
                    "length": 43,
                },
                {
                    "index": 48,
                    "marker": "+",
                    "text": " to pages missing them",
                    "length": 22,
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1
