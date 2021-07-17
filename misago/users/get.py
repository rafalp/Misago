from enum import Enum
from typing import Awaitable, List, Optional, Sequence

from ..database.paginator import Paginator
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


class UsersOrdering(str, Enum):
    JOINED_AT = "joined_at"
    USERNAME = "username"


def get_users_list(
    *,
    name: Optional[str] = None,
    email: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_moderator: Optional[bool] = None,
    is_administrator: Optional[bool] = None,
    page_size: int = 40,
    orphans: int = 0,
    order_by: UsersOrdering = UsersOrdering.JOINED_AT,
    order_desc: bool = True,
):
    query = User.query

    if is_active is not None:
        query = query.filter(is_active=is_active)
    if is_moderator is not None:
        query = query.filter(is_moderator=is_moderator)
    if is_administrator is not None:
        query = query.filter(is_administrator=is_administrator)

    return Paginator(query, page_size, orphans)
