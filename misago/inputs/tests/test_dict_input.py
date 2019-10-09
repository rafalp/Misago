from ..dictinput import DictInput
from ..stringinput import StringInput


def test_dict_input_can_be_constructed_on_initialization():
    username_input = StringInput()
    input_type = DictInput({"username": username_input})
    assert input_type.get_fields() == {"username": username_input}


def test_dict_input_can_be_constructed_programmatically():
    username_input = StringInput()

    input_type = DictInput()
    input_type.add_field("username", username_input)

    assert input_type.get_fields() == {"username": username_input}


def test_dict_input_returns_processed_input_dict():
    input_type = DictInput({"username": StringInput()})
    data, errors = input_type.process({"username": " Admin "})
    assert data == {"username": "Admin"}
    assert not errors
