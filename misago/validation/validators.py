from asyncio import gather
from typing import Any, Awaitable, Callable, Generator, List, Type, Union, cast

from pydantic import ConstrainedList, constr
from pydantic.color import Color
from pydantic.validators import list_validator

from ..conf.types import Settings
from ..utils.lists import remove_none_items
from .errors import VALIDATION_ERRORS, ListRepeatedItemsError
from .errorslist import ErrorsList

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
    except VALIDATION_ERRORS as error:
        errors.add_error(location, error)
        return None


def bulkactionidslist(item_type: Type[Any], settings: Settings) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        __args__=[item_type],
        min_items=1,
        max_items=cast(int, settings["bulk_action_limit"]),
        item_type=item_type,
    )

    return type("BulkActionIdsListValue", (BulkActionIdsList,), namespace)


CallableGenerator = Generator[Callable[..., Any], None, None]


class BulkActionIdsList(ConstrainedList):
    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        yield list_validator
        yield cls.list_length_validator
        yield cls.list_items_are_unique_validator

    @classmethod
    def list_items_are_unique_validator(cls, v):
        if len(v) != len(set(v)):
            raise ListRepeatedItemsError()
        return v


def sluggablestr(min_length: int, max_length: int) -> Type[str]:
    return constr(
        strip_whitespace=True,
        regex=r"\w|\d",
        min_length=min_length,
        max_length=max_length,
    )


def color_validator(color: Union[Color, str], *_) -> str:
    if isinstance(color, Color):
        return color.as_hex().upper()

    return Color(color).as_hex().upper()
