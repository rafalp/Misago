from ..diff import diff_text


def test_diff_text_diffs_same_content():
    result = diff_text("Lorem ipsum", "Lorem ipsum")
    assert result.lines == [
        {
            "number": 1,
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
            "number": 1,
            "marker": "-",
            "text": "Lorem ipsum",
        },
        {
            "number": 2,
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
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": None,
                    "text": "Lorem ipsu",
                },
                {
                    "marker": "-",
                    "text": "u",
                },
                {
                    "marker": None,
                    "text": "m",
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
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": None,
                    "text": "Lorem ip",
                },
                {
                    "marker": "+",
                    "text": "s",
                },
                {
                    "marker": None,
                    "text": "um",
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
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": None,
                    "text": "Lorem ip",
                },
                {
                    "marker": "-",
                    "text": "l",
                },
                {
                    "marker": "+",
                    "text": "s",
                },
                {
                    "marker": None,
                    "text": "um",
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_changed_some_characters():
    result = diff_text("Lorem islum", "Lolem iplum")
    assert result.lines == [
        {
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": None,
                    "text": "Lo",
                },
                {
                    "marker": "-",
                    "text": "r",
                },
                {
                    "marker": "+",
                    "text": "l",
                },
                {
                    "marker": None,
                    "text": "em i",
                },
                {
                    "marker": "-",
                    "text": "s",
                },
                {
                    "marker": "+",
                    "text": "p",
                },
                {
                    "marker": None,
                    "text": "lum",
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_changed_word():
    result = diff_text("Lorem ipsum dolor met", "Lorem ipsum elit met")
    assert result.lines == [
        {
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": None,
                    "text": "Lorem ipsum ",
                },
                {
                    "marker": "-",
                    "text": "dolor",
                },
                {
                    "marker": "+",
                    "text": "elit",
                },
                {
                    "marker": None,
                    "text": " met",
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
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": "-",
                    "text": "Basically",
                },
                {
                    "marker": "+",
                    "text": "If you want to go the `misago-docker` route",
                },
                {
                    "marker": None,
                    "text": ", start from there: https://misago.gitbook.io/docs/setup/misago#downloading-misago-on-the-server",
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
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": "-",
                    "text": "UI for",
                },
                {
                    "marker": "+",
                    "text": "Manage",
                },
                {
                    "marker": None,
                    "text": " private thread",
                },
                {
                    "marker": "+",
                    "text": "s",
                },
                {
                    "marker": None,
                    "text": " members",
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
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": "-",
                    "text": "U",
                },
                {
                    "marker": "+",
                    "text": "Add u",
                },
                {
                    "marker": None,
                    "text": "ser signatures",
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
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": "-",
                    "text": "M",
                },
                {
                    "marker": "+",
                    "text": "Add m",
                },
                {
                    "marker": None,
                    "text": "etatags for search engines and social sites",
                },
                {
                    "marker": "+",
                    "text": " to pages missing them",
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_real_case_5():
    result = diff_text(
        "Sometime in 2025. No promises or anything but judging by current pace, summer is most optimistic deadline, but I wouldn't be surprised if I miss it and only release after that.",
        "Sometime late in 2025. No promises or anything but judging by current pace, November is most optimistic deadline, but I wouldn't be surprised if I miss it and only release after new year of 2026.",
    )

    assert result.lines == [
        {
            "number": 1,
            "marker": "?",
            "diff": [
                {
                    "marker": None,
                    "text": "Sometime ",
                },
                {
                    "marker": "+",
                    "text": "late ",
                },
                {
                    "marker": None,
                    "text": "in 2025. No promises or anything but judging by current pace, ",
                },
                {
                    "marker": "-",
                    "text": "summ",
                },
                {
                    "marker": "+",
                    "text": "Novemb",
                },
                {
                    "marker": None,
                    "text": "er is most optimistic deadline, but I wouldn't be surprised if I miss it and only release after ",
                },
                {
                    "marker": "-",
                    "text": "that",
                },
                {
                    "marker": "+",
                    "text": "new year of 2026",
                },
                {
                    "marker": None,
                    "text": ".",
                },
            ],
        },
    ]
    assert result.added == 1
    assert result.removed == 1
