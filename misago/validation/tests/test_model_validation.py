from pydantic import BaseModel

from ..validation import validate_model


class Model(BaseModel):
    id: int
    name: str


def test_valid_input_validation_returns_valid_data():
    valid_data, _ = validate_model(Model, {"id": 123, "name": "valid"})
    assert valid_data == {"id": 123, "name": "valid"}


def test_valid_input_validation_returns_empty_errors_list():
    _, errors = validate_model(Model, {"id": 123, "name": "valid"})
    assert errors == []  # pylint: disable=use-implicit-booleaness-not-comparison


def test_partially_valid_input_validation_returns_partial_valid_data():
    valid_data, _ = validate_model(Model, {"id": "invalid", "name": "valid"})
    assert valid_data == {"name": "valid"}


def test_partially_valid_input_validation_returns_errors_list():
    _, errors = validate_model(Model, {"id": "invalid", "name": "valid"})
    assert errors
