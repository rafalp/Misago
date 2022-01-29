from typing import Sequence, Union

from .errordict import ErrorDict

ROOT_LOCATION = "__root__"


def get_error_dict(
    error: Exception, location: Union[str, Sequence[Union[str, int]]] = ROOT_LOCATION
) -> ErrorDict:
    return {
        "loc": get_error_location(location),
        "type": get_error_type(error),
        "msg": str(error),
    }


def get_error_location(location: Union[str, Sequence[Union[str, int]]]) -> str:
    """Normalize ["field_name", 0] to 'fieldName.0'."""
    if isinstance(location, (str, int)):
        return format_error_location_part(location)

    return ".".join(map(format_error_location_part, location))


def format_error_location_part(part: Union[str, int]) -> str:
    if isinstance(part, int):
        return str(part)

    if part == ROOT_LOCATION:
        return ROOT_LOCATION

    return (part[0] + part.title()[1:]).replace("_", "")


def get_error_type(error: Exception) -> str:
    if isinstance(error, AssertionError):
        return "assertion_error"

    base_name = get_error_base_name(error)
    code = (
        getattr(error, "code", None)
        or type(error).__name__.replace("Error", "").lower()
    )
    return base_name + "." + code


def get_error_base_name(error: Exception) -> str:
    if isinstance(error, ValueError):
        return "value_error"
    if isinstance(error, TypeError):
        return "type_error"

    if hasattr(error, "base_name"):
        return error.base_name  # type: ignore

    return "error"
