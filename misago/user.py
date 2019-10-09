from datetime import datetime
from typing import Any, Dict, Optional

from .database import database
from .tables import users


async def create_user(
    name, email, *, password=None, is_moderator=False, joined_at=None
) -> Dict[str, Any]:
    data = {
        "name": name,
        "slug": name.lower(),
        "email": email,
        "password": password,
        "is_moderator": is_moderator,
        "joined_at": joined_at or datetime.now(),
    }
    query = users.insert(None).values(**data)

    data["id"] = await database.execute(query)

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
