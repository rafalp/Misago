from ..templatetags.misago_metatags import mergemetatags


def test_mergemetatags_filter_merges_different_metatags():
    result = mergemetatags({"left": "start"}, {"right": "end"})
    assert list(result) == ["end", "start"]


def test_mergemetatags_filter_overrides_default_metatags():
    result = mergemetatags({"left": "start", "right": "fin"}, {"right": "end"})
    assert list(result) == ["fin", "start"]


def test_mergemetatags_filter_deletes_default_metatags():
    result = mergemetatags({"left": "start", "right": None}, {"right": "end"})
    assert list(result) == ["start"]


def test_mergemetatags_filter_handles_empty_page_metatags():
    result = mergemetatags(None, {"right": "end"})
    assert list(result) == ["end"]


def test_mergemetatags_filter_handles_empty_metatags():
    result = mergemetatags(None, None)
    assert list(result) == []
