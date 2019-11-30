import re
from typing import Any, Callable, Generator

from pydantic import ConstrainedStr
from pydantic.validators import str_validator

from .errors import UsernameError


CallableGenerator = Generator[Callable[..., Any], None, None]

USERNAME_RE = re.compile(r"^[0-9a-z]+$", re.IGNORECASE)


class UsernameStr(ConstrainedStr):
    strip_whitespace: bool = True
    strict: bool = False

    @classmethod
    def validate(cls, value: str) -> str:
        if not USERNAME_RE.match(value):
            raise UsernameError(pattern=USERNAME_RE)

        return value
