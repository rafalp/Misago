import re
from typing import Optional, Type, cast

from pydantic import ConstrainedStr, constr

from ..conf.types import Settings
from ..context import Context
from .email import get_email_hash
from .errors import (
    EmailNotAvailableError,
    UsernameError,
    UsernameNotAvailableError,
    UserNotFoundError,
)
from .loaders import users_loader
from .models import User

PASSWORD_MAX_LENGTH = 40  # Hardcoded for perf. reasons
USERNAME_RE = re.compile(r"^[0-9a-z]+$", re.IGNORECASE)


def passwordstr(settings: Settings) -> Type[str]:
    return constr(
        strip_whitespace=False,
        min_length=cast(int, settings["password_min_length"]),
        max_length=PASSWORD_MAX_LENGTH,
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


class EmailIsAvailableValidator:
    _exclude_user: Optional[int]

    def __init__(self, exclude_user: Optional[int] = None):
        self._exclude_user = exclude_user

    async def __call__(self, email: str, *_) -> str:
        email_hash = get_email_hash(email)
        query = User.query.filter(email_hash=email_hash)
        if self._exclude_user:
            query = query.exclude(id=self._exclude_user)
        if await query.exists():
            raise EmailNotAvailableError()
        return email


class UserExistsValidator:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    async def __call__(self, user_id: int, *_) -> User:
        user = await users_loader.load(self._context, user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)
        return user


class UsernameIsAvailableValidator:
    _exclude_user: Optional[int]

    def __init__(self, exclude_user: Optional[int] = None):
        self._exclude_user = exclude_user

    async def __call__(self, username: str, *_) -> str:
        query = User.query.filter(slug=username.lower())
        if self._exclude_user:
            query = query.exclude(id=self._exclude_user)
        if await query.exists():
            raise UsernameNotAvailableError()
        return username
