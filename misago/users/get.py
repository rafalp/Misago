from typing import Awaitable, Iterable, List, Optional

from .email import get_email_hash
from .models import User, UserGroup


def get_users_by_id(ids: Iterable[int]) -> Awaitable[List[User]]:
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


def get_users_by_name(names: Iterable[str]) -> Awaitable[List[User]]:
    return User.query.filter(slug__in=[s.lower() for s in names]).all()


async def get_user_by_email(email: str) -> Optional[User]:
    try:
        return await User.query.one(email_hash=get_email_hash(email))
    except User.DoesNotExist:
        return None


def get_users_groups_by_id(ids: Iterable[int]) -> Awaitable[List[UserGroup]]:
    return UserGroup.query.filter(id__in=ids).all()
