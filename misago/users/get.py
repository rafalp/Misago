from typing import Any, Dict, Optional

from ..database import database
from ..tables import users
from .email import get_email_hash


async def get_user_by_name_or_email(name_or_email: str) -> Optional[Dict[str, Any]]:
    if "@" in name_or_email:
        return await get_user_by_email(name_or_email)
    return await get_user_by_name(name_or_email)


async def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
    query = users.select().where(users.c.slug == name.lower())
    data = await database.fetch_one(query)
    return dict(**data) if data else None


async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    query = users.select().where(users.c.email_hash == get_email_hash(email))
    data = await database.fetch_one(query)
    return dict(**data) if data else None


async def get_user_by_id(
    id: int,  # pylint: disable=redefined-builtin
) -> Optional[Dict[str, Any]]:
    query = users.select().where(users.c.id == id)
    data = await database.fetch_one(query)
    return dict(**data) if data else None
