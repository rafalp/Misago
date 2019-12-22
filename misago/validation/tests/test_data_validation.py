import pytest

from pydantic import PydanticValueError

from ...errors import ErrorsList
from ..validation import ROOT_LOCATION, validate_data


VALID_VALUE = "ok"
INVALID_VALUE = "invalid"


class InvalidValueError(PydanticValueError):
    code = "invalid"
    msg_template = "invalid test data"


class OtherInvalidValueError(PydanticValueError):
    code = "invalid_other"
    msg_template = "other invalid test data"


async def validate_value(value, _):
    if value != VALID_VALUE:
        raise InvalidValueError()
    return value


async def validate_and_change_value(value, _):
    if value != VALID_VALUE:
        raise InvalidValueError()
    return "changed!"


async def validate_value_other(value, _):
    if value != VALID_VALUE:
        raise OtherInvalidValueError()
    return value


async def validate_root_value(value, errors):
    if value != {"data": VALID_VALUE}:
        raise InvalidValueError()
    return value


async def validate_and_change_root_value(value, errors):
    if value != {"data": VALID_VALUE}:
        raise InvalidValueError()
    return dict(changed=True, **value)


async def validate_root_value_local(value, errors):
    if value != {"data": VALID_VALUE}:
        errors.add_error("data", OtherInvalidValueError())
    return value


@pytest.fixture
def errors():
    return ErrorsList()


@pytest.mark.asyncio
async def test_data_is_validated_if_validator_is_specified_for_it(errors):
    _, new_errors = await validate_data(
        {"data": VALID_VALUE}, {"data": [validate_value]}, errors
    )
    assert not new_errors


@pytest.mark.asyncio
async def test_data_is_returned_if_it_passed_validation(errors):
    data, new_errors = await validate_data(
        {"data": VALID_VALUE}, {"data": [validate_value]}, errors
    )
    assert data == {"data": VALID_VALUE}
    assert not new_errors


@pytest.mark.asyncio
async def test_data_is_returned_if_validator_is_not_specified_for_it(errors):
    data, new_errors = await validate_data(
        {"data": VALID_VALUE, "other_data": True}, {"data": [validate_value]}, errors
    )
    assert data == {"data": VALID_VALUE, "other_data": True}
    assert not new_errors


@pytest.mark.asyncio
async def test_invalid_data_errors_are_added_to_errors_list(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE}, {"data": [validate_value]}, errors
    )
    assert new_errors
    assert new_errors.get_errors_locations() == ["data"]
    assert new_errors.get_errors_types() == ["value_error.invalid"]


@pytest.mark.asyncio
async def test_validator_can_change_validated_value(errors):
    data, new_errors = await validate_data(
        {"data": VALID_VALUE}, {"data": [validate_and_change_value]}, errors
    )
    assert data == {"data": "changed!"}
    assert not new_errors


@pytest.mark.asyncio
async def test_validation_is_interrupted_at_first_validation_error(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE},
        {"data": [validate_value, validate_value_other]},
        errors,
    )
    assert new_errors
    assert new_errors.get_errors_locations() == ["data"]
    assert new_errors.get_errors_types() == [
        "value_error.invalid",
    ]


@pytest.mark.asyncio
async def test_root_validators_are_ran_data(errors):
    _, new_errors = await validate_data(
        {"data": VALID_VALUE}, {ROOT_LOCATION: [validate_root_value]}, errors,
    )
    assert not new_errors


@pytest.mark.asyncio
async def test_root_validators_errors_are_added_to_errors_list(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE}, {ROOT_LOCATION: [validate_root_value]}, errors,
    )
    assert new_errors
    assert new_errors.get_errors_locations() == [ROOT_LOCATION]
    assert new_errors.get_errors_types() == ["value_error.invalid"]


@pytest.mark.asyncio
async def test_root_validators_can_customize_errors_location(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE}, {ROOT_LOCATION: [validate_root_value_local]}, errors,
    )
    assert new_errors
    assert new_errors.get_errors_locations() == ["data"]
    assert new_errors.get_errors_types() == ["value_error.invalid_other"]


@pytest.mark.asyncio
async def test_root_validators_are_ran_for_completely_invalid_data(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE},
        {"data": [validate_value], ROOT_LOCATION: [validate_root_value]},
        errors,
    )
    assert new_errors
    assert new_errors.get_errors_locations() == ["data", ROOT_LOCATION]
    assert new_errors.get_errors_types() == [
        "value_error.invalid",
        "value_error.invalid",
    ]


@pytest.mark.asyncio
async def test_root_validators_are_ran_for_partially_valid_data(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE, "valid_data": "ok!"},
        {"data": [validate_value], ROOT_LOCATION: [validate_root_value]},
        errors,
    )
    assert new_errors
    assert new_errors.get_errors_locations() == ["data", ROOT_LOCATION]
    assert new_errors.get_errors_types() == [
        "value_error.invalid",
        "value_error.invalid",
    ]


@pytest.mark.asyncio
async def test_root_validators_is_interrupted_on_first_error(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE},
        {ROOT_LOCATION: [validate_root_value, validate_and_change_root_value]},
        errors,
    )
    assert new_errors
    assert new_errors.get_errors_locations() == [ROOT_LOCATION]
    assert new_errors.get_errors_types() == ["value_error.invalid"]


@pytest.mark.asyncio
async def test_root_validators_can_change_validated_data(errors):
    data, new_errors = await validate_data(
        {"data": VALID_VALUE},
        {ROOT_LOCATION: [validate_and_change_root_value]},
        errors,
    )
    assert data == {"data": VALID_VALUE, "changed": True}
    assert not new_errors


@pytest.mark.asyncio
async def test_original_errors_list_is_not_mutated_by_validator(errors):
    _, new_errors = await validate_data(
        {"data": INVALID_VALUE}, {"data": [validate_value]}, errors
    )
    assert new_errors != errors
