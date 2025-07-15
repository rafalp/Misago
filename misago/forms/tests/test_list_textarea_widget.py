from django.http import QueryDict

from ..widgets import ListTextarea


def test_list_textarea_widget_value_from_datadict_returns_empty_list():
    widget = ListTextarea()
    assert widget.value_from_datadict(QueryDict(""), None, "name") == []


def test_list_textarea_widget_value_from_datadict_returns_list():
    widget = ListTextarea()
    assert widget.value_from_datadict(
        QueryDict("name=  \nhello\n\n  World  \nhello"), None, "name"
    ) == ["  ", "hello", "", "  World  ", "hello"]
