from asyncio import gather
from typing import Any, Awaitable, Callable, List, Union

from pydantic.color import Color

from ..errors import ErrorsList
from ..utils.lists import remove_none_items

Validator = Callable[[Any, ErrorsList, str], Union[Awaitable[Any], Any]]


class BulkValidator:
    _validators: List[Validator]

    def __init__(self, validators: List[Validator]):
        self._validators = validators

    async def __call__(
        self, items: List[Any], errors: ErrorsList, field_name: str
    ) -> List[Any]:
        validators = []
        for i, item in enumerate(items):
            validators.append(
                _validate_bulk_item(
                    [field_name, str(i)], item, self._validators, errors
                )
            )

        if validators:
            validated_items = await gather(*validators)
            return remove_none_items(validated_items)

        return []


async def _validate_bulk_item(
    location: List[str], data: Any, validators: List[Validator], errors: ErrorsList
) -> Any:
    try:
        for validator in validators:
            data = await validator(data, errors, location[0])
        return data
    except Exception as error:
        errors.add_error(location, error)
        return None


def color_validator(color: Union[Color, str], *_) -> str:
    if isinstance(color, Color):
        return color.as_hex().upper()

    return Color(color).as_hex().upper()
