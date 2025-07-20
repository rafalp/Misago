from django.http import QueryDict

from ..widgets import ListInput


def test_list_input_widget_value_from_datadict_returns_empty_list():
    widget = ListInput()
    assert widget.value_from_datadict(QueryDict(""), None, "name") == []


def test_list_input_widget_value_from_datadict_returns_list():
    widget = ListInput()
    assert widget.value_from_datadict(
        QueryDict("name=A&name=B&name=&name=&name=A&name=  C  "), None, "name"
    ) == ["A", "B", "A", "  C  "]
