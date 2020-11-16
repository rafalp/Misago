import pytest
from django.core.exceptions import ValidationError

from ..validators import validate_image_square, validate_sluggable


def test_sluggable_validator_raises_error_if_result_slug_will_be_empty():
    validator = validate_sluggable()
    with pytest.raises(ValidationError):
        validator("!#@! !@#@")


def test_sluggable_validator_raises_custom_error_if_result_slug_will_be_empty():
    error_message = "I'm short custom error!"
    validator = validate_sluggable(error_short=error_message)
    with pytest.raises(ValidationError) as e:
        validator("!#@! !@#@")
    assert error_message in str(e.value)


def test_sluggable_validator_raises_error_if_result_slug_will_be_too_long():
    validator = validate_sluggable()
    with pytest.raises(ValidationError):
        validator("a" * 256)


def test_sluggable_validator_raises_custom_error_if_result_slug_will_be_too_long():
    error_message = "I'm long custom error!"
    validator = validate_sluggable(error_long=error_message)
    with pytest.raises(ValidationError) as e:
        validator("a" * 256)
    assert error_message in str(e.value)


def test_square_square_validator_validates_square_image(mocker):
    image = mocker.Mock(width=100, height=100)
    validate_image_square(image)


def test_square_square_validator_raises_error_if_image_is_not_square(mocker):
    image = mocker.Mock(width=100, height=200)
    with pytest.raises(ValidationError):
        validate_image_square(image)
