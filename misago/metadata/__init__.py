from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..users.models import User


@dataclass
class TextMetadata:
    type = "text"

    id: str
    text: str
    icon: str | None = None
    url: str | None = None
    aria_label: str | None = None


@dataclass
class DatetimeMetadata:
    type = "datetime"

    id: str
    text: str
    datetime: datetime
    is_sentence: bool = False
    url: str | None = None
    icon: str | None = None
    aria_label: str | None = None


@dataclass
class NumberMetadata:
    type = "number"

    id: str
    text: str
    number: int
    icon: str | None = None
    aria_label: str | None = None


@dataclass
class UserDatetimeMetadata:
    type = "user_datetime"

    id: str
    user: Union["User", str]
    datetime: datetime
    url: str | None = None
    aria_label: str | None = None

    @property
    def is_anonymous_user(self) -> bool:
        return isinstance(self.user, str)

    @property
    def is_registered_user(self) -> bool:
        return not isinstance(self.user, str)
