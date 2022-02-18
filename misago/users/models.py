from dataclasses import dataclass
from datetime import datetime
from typing import Any, Awaitable, Dict, List, Optional

from ..avatars.store import delete_user_avatars
from ..avatars.types import AvatarType
from ..context import Context
from ..database import Model, ObjectMapperQuery, model_registry, register_model
from ..passwords import check_password, hash_password
from ..tables import users
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
    avatar_type: AvatarType
    avatars: List[dict]
    is_active: bool
    is_moderator: bool
    is_admin: bool
    joined_at: datetime
    extra: dict

    @property
    def posts_query(self) -> ObjectMapperQuery:
        return model_registry["Post"].filter(poster_id=self.id)

    @property
    def threads_query(self) -> ObjectMapperQuery:
        return model_registry["Thread"].filter(starter_id=self.id)

    @classmethod
    async def create(
        cls,
        name: str,
        email: str,
        *,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        avatar_type: Optional[AvatarType] = None,
        avatars: Optional[List[dict]] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[Context] = None,
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
            "avatar_type": avatar_type or AvatarType.GRAVATAR,
            "avatars": avatars or [],
            "is_active": is_active,
            "is_moderator": is_moderator,
            "is_admin": is_admin,
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
        avatar_type: Optional[AvatarType] = None,
        avatars: Optional[List[dict]] = None,
        is_active: Optional[bool] = None,
        is_moderator: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[Context] = None,
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

        if avatar_type is not None and avatar_type != self.avatar_type:
            changes["avatar_type"] = avatar_type

        if avatars is not None and avatars != self.avatars:
            changes["avatars"] = avatars

        if is_active is not None and is_active != self.is_active:
            changes["is_active"] = is_active

        if is_moderator is not None and is_moderator != self.is_moderator:
            changes["is_moderator"] = is_moderator

        if is_admin is not None and is_admin != self.is_admin:
            changes["is_admin"] = is_admin

        if joined_at is not None and joined_at != self.joined_at:
            changes["joined_at"] = joined_at

        if extra is not None and extra != self.extra:
            changes["extra"] = extra

        if not changes:
            return self

        await User.query.filter(id=self.id).update(**changes)

        return self.replace(**changes)

    async def delete(self):
        await delete_user_avatars(self)
        return await User.query.filter(id=self.id).delete()

    async def check_password(self, password: str) -> bool:
        if not self.password:
            return False

        return await check_password(password, self.password)
