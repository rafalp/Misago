from datetime import datetime
from typing import Any, Dict, Optional

from .database import database, queries
from .passwords import hash_password
from .tables import users


async def create_user(
    name: str,
    email: str,
    *,
    password: Optional[str] = None,
    is_moderator: bool = False,
    joined_at: Optional[datetime] = None
) -> Dict[str, Any]:
    password_hash = None
    if password:
        password_hash = await hash_password(password)

    data: Dict[str, Any] = {
        "name": name,
        "slug": name.lower(),
        "email": email,
        "password": password_hash,
        "is_moderator": is_moderator,
        "joined_at": joined_at or datetime.now(),
    }

    data["id"] = await queries.insert(users, **data)

    return data


async def get_user_by_name_or_email(name_or_email: str) -> Optional[Dict[str, Any]]:
    if "@" in name_or_email:
        return await get_user_by_email(name_or_email)
    return await get_user_by_name(name_or_email)


async def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
    query = users.select().where(users.c.slug == name)
    data = await database.fetch_one(query)
    return dict(**data) if data else None


async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    query = users.select().where(users.c.email == email)
    data = await database.fetch_one(query)
    return dict(**data) if data else None


async def get_user_by_id(
    id: int  # pylint: disable=redefined-builtin
) -> Optional[Dict[str, Any]]:
    query = users.select().where(users.c.id == id)
    data = await database.fetch_one(query)
    return dict(**data) if data else None
