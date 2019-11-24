from asyncio import gather
from typing import Any, Dict, List, Tuple, Type, cast

from pydantic import (
    BaseModel,
    PydanticTypeError,
    PydanticValueError,
    validate_model as pydantic_validate_model,
)

from ..types import AsyncRootValidator, AsyncValidator
from .errorslist import ROOT_LOCATION, ErrorsList


def validate_model(
    model: Type[BaseModel], input_data: Dict[str, Any]
) -> Tuple[Dict[str, Any], ErrorsList]:
    """Wrapper for pydantic.validate_model that always returns list for errors."""
    validated_data, _, errors = pydantic_validate_model(model, input_data)
    if not errors:
        return validated_data, ErrorsList()
    return validated_data, ErrorsList(errors.errors())


async def validate_data(
    validated_data: Dict[str, Any],
    validators: Dict[str, List[AsyncValidator]],
    errors: ErrorsList,
) -> ErrorsList:
    new_errors = ErrorsList()
    validators_queue = []
    for field_name, field_validators in validators.items():
        if field_name not in validated_data:
            continue

        for validator in field_validators:
            validators_queue.append(
                validate_field_data(
                    field_name, validated_data[field_name], validator, new_errors
                )
            )

    if ROOT_LOCATION in validators:
        for validator in validators[ROOT_LOCATION]:
            validator = cast(AsyncRootValidator, validator)
            validators_queue.append(validator(validated_data, new_errors))

    if validators_queue:
        await gather(*validators_queue)

    return errors + new_errors


async def validate_field_data(
    field_name: str, data: Any, validator: AsyncValidator, errors: ErrorsList
):
    try:
        await validator(data)
    except (PydanticTypeError, PydanticValueError) as error:
        errors.add_error(field_name, error)
