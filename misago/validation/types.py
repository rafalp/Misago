import re
from typing import Any, Callable, Generator, Type, cast

from pydantic import ConstrainedStr, constr

from ..errors import UsernameError
from ..types import Settings


CallableGenerator = Generator[Callable[..., Any], None, None]

PASSWORD_MAX_LENGTH = 40  # Hardcoded for perf. reasons
USERNAME_RE = re.compile(r"^[0-9a-z]+$", re.IGNORECASE)


def passwordstr(settings: Settings) -> Type[str]:
    return constr(
        strip_whitespace=False,
        min_length=cast(int, settings["password_min_length"]),
        max_length=PASSWORD_MAX_LENGTH,
    )


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


class UsernameStr(ConstrainedStr):
    strip_whitespace: bool = True
    strict: bool = False

    @classmethod
    def validate(cls, value: str) -> str:
        if not USERNAME_RE.match(value):
            raise UsernameError(pattern=cast(str, USERNAME_RE))

        return value


def usernamestr(settings: Settings) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        min_length=cast(int, settings["username_min_length"]),
        max_length=cast(int, settings["username_max_length"]),
    )

    return type("UsernameStrValue", (UsernameStr,), namespace)
