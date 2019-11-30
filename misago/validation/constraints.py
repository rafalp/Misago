import re
from typing import Type, cast

from pydantic import constr

from ..types import Settings
from .fields import UsernameStr


PASSWORD_MAX_LENGTH = 40  # Hardcoded for perf. reasons


def passwordstr(settings: Settings) -> Type[str]:
    return constr(
        strip_whitespace=False,
        min_length=cast(int, settings["password_min_length"]),
        max_length=PASSWORD_MAX_LENGTH,
    )


def usernamestr(settings: Settings) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        min_length=cast(int, settings["username_min_length"]),
        max_length=cast(int, settings["username_max_length"]),
    )

    return type("UsernameStrValue", (UsernameStr,), namespace)
