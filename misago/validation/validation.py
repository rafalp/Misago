from asyncio import gather
from typing import Any, Dict, List, Tuple, Type, Union, cast

from pydantic import (
    BaseModel,
    PydanticTypeError,
    PydanticValueError,
    validate_model as pydantic_validate_model,
)

from ..errors import AuthError, ErrorsList
from ..types import AsyncRootValidator, AsyncValidator


ROOT_LOCATION = ErrorsList.ROOT_LOCATION


def validate_model(
    model: Type[BaseModel], input_data: Dict[str, Any]
) -> Tuple[Dict[str, Any], ErrorsList]:
    """Wrapper for pydantic.validate_model that always returns list for errors."""
    validated_data, _, errors = pydantic_validate_model(model, input_data)
    if not errors:
        return validated_data, ErrorsList()
    return validated_data, ErrorsList(cast(ErrorsList, errors.errors()))


async def validate_data(
    validated_data: Dict[str, Any],
    validators: Dict[str, List[Union[AsyncRootValidator, AsyncValidator]]],
    errors: ErrorsList,
) -> ErrorsList:
    new_errors = ErrorsList()
    validators_queue = []
    for field_name, field_validators in validators.items():
        if field_name not in validated_data:
            continue

        for validator in field_validators:
            validator = cast(AsyncValidator, validator)
            validators_queue.append(
                validate_field_data(
                    field_name, validated_data[field_name], validator, new_errors
                )
            )

    if ROOT_LOCATION in validators:
        for root_validator in validators[ROOT_LOCATION]:
            root_validator = cast(AsyncRootValidator, root_validator)
            validators_queue.append(
                validate_root_data(validated_data, root_validator, new_errors)
            )

    if validators_queue:
        await gather(*validators_queue)

    return errors + new_errors


async def validate_field_data(
    field_name: str, data: Any, validator: AsyncValidator, errors: ErrorsList
):
    try:
        await validator(data)
    except (AuthError, PydanticTypeError, PydanticValueError) as error:
        errors.add_error(field_name, error)


async def validate_root_data(
    data: Any, validator: AsyncRootValidator, errors: ErrorsList
):
    try:
        await validator(data, errors)
    except (AuthError, PydanticTypeError, PydanticValueError) as error:
        errors.add_root_error(error)
