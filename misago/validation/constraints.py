import re
from typing import Type, cast

from pydantic import constr

from ..types import Settings


PASSWORD_MAX_LENGTH = 40  # Hardcoded for perf. reasons
USERNAME_RE = re.compile(r"^[0-9a-z]+$", re.IGNORECASE)


def passwordstr(settings: Settings) -> Type[str]:
    return constr(
        strip_whitespace=False,
        min_length=cast(int, settings["password_min_length"]),
        max_length=PASSWORD_MAX_LENGTH,
    )


def usernamestr(settings: Settings) -> Type[str]:
    return constr(
        strip_whitespace=True,
        min_length=cast(int, settings["username_min_length"]),
        max_length=cast(int, settings["username_max_length"]),
        regex=cast(str, USERNAME_RE),
    )
