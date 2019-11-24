import re
from typing import Type

from pydantic import constr

from ..types import Settings


PASSWORD_MAX_LENGTH = 40  # Hardcoded for
USERNAME_RE = re.compile(r"^[0-9a-z]+$", re.IGNORECASE)


def passwordstr(settings: Settings) -> Type[str]:
    return constr(
        strip_whitespace=False,
        min_length=settings["password_min_length"],
        max_length=PASSWORD_MAX_LENGTH,
    )


def usernamestr(settings: Settings) -> Type[str]:
    return constr(
        strip_whitespace=True,
        min_length=settings["username_min_length"],
        max_length=settings["username_max_length"],
        regex=USERNAME_RE,
    )
