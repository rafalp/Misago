from dataclasses import dataclass
from datetime import datetime
from typing import Any, Awaitable, Dict, Optional

from ..database import MapperQuery, Model, model_registry, register_model
from ..passwords import hash_password
from ..tables import users
from ..graphql import GraphQLContext
from ..utils import timezone
from ..utils.strings import slugify
from .email import get_email_hash, normalize_email


@register_model("User", users)
@dataclass
class User(Model):
    id: int
    name: str
    slug: str
    email: str
    email_hash: str
    full_name: Optional[str]
    password: Optional[str]
    is_active: bool
    is_moderator: bool
    is_administrator: bool
    joined_at: datetime
    extra: dict

    @property
    def posts_query(self) -> MapperQuery:
        return model_registry["Post"].filter(poster_id=self.id)

    @property
    def threads_query(self) -> MapperQuery:
        return model_registry["Thread"].filter(starter_id=self.id)

    @classmethod
    async def create(
        cls,
        name: str,
        email: str,
        *,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_administrator: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable["User"]:
        password_hash = None
        if password:
            password_hash = await hash_password(password)

        data: Dict[str, Any] = {
            "name": name,
            "slug": slugify(name),
            "email": normalize_email(email),
            "email_hash": get_email_hash(email),
            "full_name": full_name,
            "password": password_hash,
            "is_active": is_active,
            "is_moderator": is_moderator,
            "is_administrator": is_administrator,
            "joined_at": joined_at or timezone.now(),
            "extra": extra or {},
        }

        return await cls.query.insert(**data)

    async def update(
        self,
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
    ) -> "User":
        changes: Dict[str, Any] = {}

        if name is not None and name != self.name:
            changes["name"] = name
            changes["slug"] = slugify(name)

        if email is not None and normalize_email(email) != self.email:
            changes["email"] = normalize_email(email)
            changes["email_hash"] = get_email_hash(email)

        if full_name is not None and full_name != self.full_name:
            changes["full_name"] = full_name or None

        if password is not None:
            changes["password"] = await hash_password(password)

        if is_active is not None and is_active != self.is_active:
            changes["is_active"] = is_active

        if is_moderator is not None and is_moderator != self.is_moderator:
            changes["is_moderator"] = is_moderator

        if is_administrator is not None and is_administrator != self.is_administrator:
            changes["is_administrator"] = is_administrator

        if joined_at is not None and joined_at != self.joined_at:
            changes["joined_at"] = joined_at

        if extra is not None and extra != self.extra:
            changes["extra"] = extra

        if not changes:
            return self

        await User.query.filter(id=self.id).update(**changes)

        return self.replace(**changes)

    def delete(self):
        return User.query.filter(id=self.id).delete()
