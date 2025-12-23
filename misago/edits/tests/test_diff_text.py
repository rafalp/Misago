from ..diff import diff_text


def test_diff_text_diffs_same_content():
    result = diff_text("Lorem ipsum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": None,
            "text": "Lorem ipsum",
            "changed": [],
            "added": [],
            "removed": [],
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
            "changed": [],
            "added": [],
            "removed": [],
        },
        {
            "marker": "+",
            "text": "Dolor met",
            "changed": [],
            "added": [],
            "removed": [],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_removed_characters():
    result = diff_text("Lorem ipsuum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": "-",
            "text": "Lorem ipsuum",
            "changed": [],
            "added": [],
            "removed": [10],
        },
        {
            "marker": "+",
            "text": "Lorem ipsum",
            "changed": [],
            "added": [],
            "removed": [],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_added_characters():
    result = diff_text("Lorem ipum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": "-",
            "text": "Lorem ipum",
            "changed": [],
            "added": [],
            "removed": [],
        },
        {
            "marker": "+",
            "text": "Lorem ipsum",
            "changed": [],
            "added": [8],
            "removed": [],
        },
    ]
    assert result.added == 1
    assert result.removed == 1


def test_diff_text_diffs_changed_characters():
    result = diff_text("Lorem iplum", "Lorem ipsum")
    assert result.lines == [
        {
            "marker": "-",
            "text": "Lorem iplum",
            "changed": [8],
            "added": [],
            "removed": [],
        },
        {
            "marker": "+",
            "text": "Lorem ipsum",
            "changed": [8],
            "added": [],
            "removed": [],
        },
    ]
    assert result.added == 1
    assert result.removed == 1
