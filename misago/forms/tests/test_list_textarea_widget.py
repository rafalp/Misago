from django.http import QueryDict

from ..widgets import ListTextarea


def test_list_textarea_widget_value_from_datadict_returns_empty_list():
    widget = ListTextarea()
    assert widget.value_from_datadict(QueryDict(""), None, "name") == []


def test_list_textarea_widget_value_from_datadict_returns_list():
    widget = ListTextarea()
    assert widget.value_from_datadict(
        QueryDict("name=  \nhello\n\n  World  \nhello"), None, "name"
    ) == ["hello", "  World  ", "hello"]


def test_list_textarea_widget_format_value_joins_lines_as_str():
    widget = ListTextarea()
    assert widget.format_value(["A", "B", "C"]) == "A\nB\nC"


def test_list_textarea_widget_format_value_returns_none_for_no_value():
    widget = ListTextarea()
    assert widget.format_value(None) is None
