from typing import Awaitable, List, Optional, Sequence

from .email import get_email_hash
from .models import User


def get_users_by_id(ids: Sequence[int]) -> Awaitable[List[User]]:
    return User.query.filter(id__in=ids).all()


async def get_user_by_name_or_email(name_or_email: str) -> Optional[User]:
    if "@" in name_or_email:
        return await get_user_by_email(name_or_email)
    return await get_user_by_name(name_or_email)


async def get_user_by_name(name: str) -> Optional[User]:
    try:
        return await User.query.one(slug=name.lower())
    except User.DoesNotExist:
        return None


def get_users_by_name(names: Sequence[str]) -> Awaitable[List[User]]:
    return User.query.filter(slug__in=[s.lower() for s in names]).all()


async def get_user_by_email(email: str) -> Optional[User]:
    try:
        return await User.query.one(email_hash=get_email_hash(email))
    except User.DoesNotExist:
        return None
