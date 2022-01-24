from typing import Any, Callable, Generator, Type, cast

from pydantic import ConstrainedList, constr
from pydantic.validators import list_validator

from ..conf.types import Settings
from ..errors import ListRepeatedItemsError

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


def bulkactionidslist(item_type: Type[Any], settings: Settings) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        __args__=[item_type],
        min_items=1,
        max_items=cast(int, settings["bulk_action_limit"]),
        item_type=item_type,
    )

    return type("BulkActionIdsListValue", (BulkActionIdsList,), namespace)


def sluggablestr(min_length: int, max_length: int) -> Type[str]:
    return constr(
        strip_whitespace=True,
        regex=r"\w|\d",
        min_length=min_length,
        max_length=max_length,
    )


def threadtitlestr(settings: Settings) -> Type[str]:
    return sluggablestr(
        min_length=cast(int, settings["thread_title_min_length"]),
        max_length=cast(int, settings["thread_title_max_length"]),
    )
