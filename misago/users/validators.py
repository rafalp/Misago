from typing import Optional, Union

from ..graphql import GraphQLContext
from ..loaders import load_user
from .email import get_email_hash
from .errors import EmailNotAvailableError, UsernameNotAvailableError, UserNotFoundError
from .models import User

PASSWORD_MAX_LENGTH = 40  # Hardcoded for perf. reasons


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
    _context: GraphQLContext

    def __init__(self, context: GraphQLContext):
        self._context = context

    async def __call__(self, user_id: Union[int, str], *_) -> User:
        user = await load_user(self._context, user_id)
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
