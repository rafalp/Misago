from dataclasses import replace
from datetime import datetime
from typing import Any, Dict, Optional

from ..database.queries import update
from ..graphql import GraphQLContext
from ..passwords import hash_password
from ..tables import users
from ..utils.strings import slugify
from .email import get_email_hash, normalize_email
from .models import User


async def update_user(
    user: User,
    *,
    name: Optional[str] = None,
    email: Optional[str] = None,
    full_name: Optional[str] = None,
    password: Optional[str] = None,
    is_active: bool = True,
    is_moderator: bool = False,
    is_administrator: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None,
    context: Optional[GraphQLContext] = None,
) -> User:
    changes: Dict[str, Any] = {}

    if name is not None and name != user.name:
        changes["name"] = name
        changes["slug"] = slugify(name)

    if email is not None and normalize_email(email) != user.email:
        changes["email"] = normalize_email(email)
        changes["email_hash"] = get_email_hash(email)

    if full_name is not None and full_name != user.full_name:
        changes["full_name"] = full_name or None

    if password is not None:
        changes["password"] = await hash_password(password)

    if is_active is not None and is_active != user.is_active:
        changes["is_active"] = is_active

    if is_moderator is not None and is_moderator != user.is_moderator:
        changes["is_moderator"] = is_moderator

    if is_administrator is not None and is_administrator != user.is_administrator:
        changes["is_administrator"] = is_administrator

    if joined_at is not None and joined_at != user.joined_at:
        changes["joined_at"] = joined_at

    if extra is not None and extra != user.extra:
        changes["extra"] = extra

    if not changes:
        return user

    await update(users, user.id, **changes)

    updated_user = replace(user, **changes)
    return updated_user
