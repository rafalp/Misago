from asyncio import gather
from typing import Any, Dict, Sequence, Tuple, Type, Union

from pydantic import (
    BaseModel,
    PydanticTypeError,
    PydanticValueError,
    validate_model as pydantic_validate_model,
)

from ..types import ErrorsList


def validate_model(
    model: Type[BaseModel], input_data: Dict[str, Any]
) -> Tuple[Dict[str, Any], ErrorsList]:
    """Wrapper for pydantic.validate_model that always returns list for errors."""
    validated_data, _, errors = pydantic_validate_model(model, input_data)
    if not errors:
        return validated_data, []
    return validated_data, errors.errors()


async def validate_data(valid_data: Dict[str, Any], validators) -> ErrorsList:
    errors: ErrorsList = []
    validators_to_run = []
    for field_name, validators in validators.items():
        if field_name not in valid_data:
            continue

        for validator in validators:
            validators_to_run.append(
                wrap_field_data_validator(
                    field_name, valid_data[field_name], validator, errors
                )
            )

    if validators_to_run:
        await gather(*validators_to_run)

    return errors


def wrap_field_data_validator(
    field_name: str, data: Any, validator, errors: ErrorsList
):
    async def validate_field():
        try:
            await validator(data)
        except (TypeError, ValueError) as error:
            add_error_to_list(errors, field_name, error)

    return validate_field


def add_error_to_list(
    errors: ErrorsList,
    location: str,
    error: Union[PydanticTypeError, PydanticValueError],
):
    errors.append(
        {"loc": (location,), "msg": error.msg_template, "type": error.code,}
    )
