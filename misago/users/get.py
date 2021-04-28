from typing import List, Optional, Sequence

from ..database import database
from ..tables import users
from .email import get_email_hash
from .models import User


async def get_user_by_id(user_id: int) -> Optional[User]:
    query = users.select().where(users.c.id == user_id)
    data = await database.fetch_one(query)
    return User(**data) if data else None


async def get_users_by_id(ids: Sequence[int]) -> List[User]:
    query = users.select().where(users.c.id.in_(ids))
    data = await database.fetch_all(query)
    return [User(**row) for row in data]


async def get_user_by_name_or_email(name_or_email: str) -> Optional[User]:
    if "@" in name_or_email:
        return await get_user_by_email(name_or_email)
    return await get_user_by_name(name_or_email)


async def get_user_by_name(name: str) -> Optional[User]:
    query = users.select().where(users.c.slug == name.lower())
    data = await database.fetch_one(query)
    return User(**data) if data else None


async def get_users_by_name(names: Sequence[str]) -> List[User]:
    query = users.select().where(users.c.slug.in_([s.lower() for s in names]))
    data = await database.fetch_all(query)
    return [User(**row) for row in data]


async def get_user_by_email(email: str) -> Optional[User]:
    query = users.select().where(users.c.email_hash == get_email_hash(email))
    data = await database.fetch_one(query)
    return User(**data) if data else None
