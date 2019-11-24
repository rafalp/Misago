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


def add_error_to_list(
    errors: ErrorsList,
    location: Union[str, Sequence[Union[str, int]]],
    error: Union[PydanticTypeError, PydanticValueError],
):
    if isinstance(location, str):
        location = (location,)

    errors.append(
        {"loc": tuple(location), "msg": error.msg_template, "type": error.code,}
    )
