from typing import Optional

from sqlalchemy.sql import select

from ..database import database
from ..errors import EmailIsNotAvailableError, UsernameIsNotAvailableError
from ..tables import users
from ..types import AsyncValidator
from ..users.email import get_email_hash


def validate_email_is_available(exclude_user: Optional[int] = None) -> AsyncValidator:
    async def validate_email_is_available_in_db(email):
        email_hash = get_email_hash(email)
        query = select([users.c.id]).where(users.c.email_hash == email_hash)
        if exclude_user:
            query = query.where(users.c.id != exclude_user)

        if await database.fetch_one(query):
            raise EmailIsNotAvailableError()

    return validate_email_is_available_in_db


def validate_username_is_available(
    exclude_user: Optional[int] = None,
) -> AsyncValidator:
    async def validate_username_is_available_in_db(username):
        query = select([users.c.id]).where(users.c.slug == username.lower())
        if exclude_user:
            query = query.where(users.c.id != exclude_user)

        if await database.fetch_one(query):
            raise UsernameIsNotAvailableError()

    return validate_username_is_available_in_db
