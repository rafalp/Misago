from ..stringinput import StringInput


def test_string_input_proceessing_fails_if_value_is_required_and_none():
    input_type = StringInput(required=True)
    data, errors = input_type.process(None)
    assert data is None
    assert errors.unwrap() == ["REQUIRED"]


def test_string_input_proceessing_passess_if_value_is_required_and_not_none():
    input_type = StringInput(required=True)
    data, errors = input_type.process("ok")
    assert data == "ok"
    assert not errors


def test_string_input_proceessing_passess_if_value_is_not_required_and_none():
    input_type = StringInput(required=False)
    data, errors = input_type.process(None)
    assert data is None
    assert not errors


def test_string_input_proceessing_fails_if_value_is_required_and_cant_be_empty():
    input_type = StringInput(required=True, allow_empty=False)
    data, errors = input_type.process("")
    assert data is None
    assert errors.unwrap() == ["EMPTY"]


def test_string_input_proceessing_passess_if_value_is_required_and_can_be_empty():
    input_type = StringInput(required=True, allow_empty=True)
    data, errors = input_type.process("")
    assert data == ""
    assert not errors


def test_string_input_proceessing_strips_whitespace_if_strip_is_enabled():
    input_type = StringInput(strip=True)
    data, errors = input_type.process(" ok ")
    assert data == "ok"
    assert not errors


def test_string_input_proceessing_preserves_whitespace_if_strip_is_disabled():
    input_type = StringInput(strip=False)
    data, errors = input_type.process(" ok ")
    assert data == " ok "
    assert not errors
