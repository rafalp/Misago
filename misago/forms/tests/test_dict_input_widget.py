from django.http import QueryDict

from ..widgets import DictInput


def test_dict_input_widget_value_from_datadict_returns_empty_dict():
    widget = DictInput()
    assert widget.value_from_datadict(QueryDict(""), None, "name") == {}


def test_dict_input_widget_value_from_datadict_returns_dict():
    widget = DictInput()
    assert widget.value_from_datadict(
        QueryDict("name[1]=A&name[2]=&name[3]=&name[4]=A&name[wow]=  C  "), None, "name"
    ) == {
        "1": "A",
        "2": "",
        "3": "",
        "4": "A",
        "wow": "  C  ",
    }


def test_dict_input_widget_value_from_datadict_skips_invalid_keys():
    widget = DictInput()
    assert widget.value_from_datadict(
        QueryDict("name=A&name[]=B&name[a]=valid"), None, "name"
    ) == {"a": "valid"}
