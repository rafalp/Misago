from asyncio import gather
from typing import Any, Dict, List, Optional, Tuple, Type, cast

from pydantic import (
    BaseModel,
    PydanticTypeError,
    PydanticValueError,
    validate_model as pydantic_validate_model,
)

from ..errors import AuthError, ErrorsList
from ..types import AsyncValidator


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
    model_data: Dict[str, Any],
    validators: Dict[str, List[AsyncValidator]],
    errors: ErrorsList,
) -> Tuple[Dict[str, Any], ErrorsList]:
    if not model_data or not validators:
        return model_data, errors

    new_errors = ErrorsList()
    validated_data: Dict[str, Any] = {}

    validators_queue = []
    validators_queue_fields = []
    for field_name, field_data in model_data.items():
        if validators.get(field_name) and field_data is not None:
            field_validators = validators[field_name]
            validators_queue_fields.append(field_name)
            validators_queue.append(
                validate_field_data(
                    field_name, field_data, field_validators, new_errors
                )
            )
        else:
            validated_data[field_name] = field_data

    if validators_queue:
        for i, validated_field_data in enumerate(await gather(*validators_queue)):
            validated_field_name = validators_queue_fields[i]
            if validated_field_data is not None:
                validated_data[validated_field_name] = validated_field_data

    if ROOT_LOCATION in validators:
        for root_validator in validators[ROOT_LOCATION]:
            try:
                validated_data = await root_validator(
                    validated_data, new_errors, ROOT_LOCATION
                )
            except (AuthError, PydanticTypeError, PydanticValueError) as error:
                new_errors.add_root_error(error)

    return validated_data, errors + new_errors


async def validate_field_data(
    field_name: str, data: Any, validators: List[AsyncValidator], errors: ErrorsList,
) -> Optional[Any]:
    try:
        for validator in validators:
            data = await validator(data, errors, field_name)
        return data
    except (AuthError, PydanticTypeError, PydanticValueError) as error:
        errors.add_error(field_name, error)
        return None
