from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..database import Model, register_model
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
    ) -> "User":
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

    async def update() -> "User":
        pass

    def delete(self):
        return User.query.filter(id=self.id).delete()