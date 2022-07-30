from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, cast

from sqlalchemy import select

from ..avatars.store import delete_user_avatars
from ..avatars.types import AvatarType
from ..context import Context
from ..database import database
from ..database.models import Model, Query, mapper_registry, register_model
from ..passwords import check_password, hash_password
from ..tables import user_groups, user_group_memberships, users
from ..utils import timezone
from ..utils.strings import slugify
from .aclkey import create_acl_key
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
    group_id: int
    acl_key: str
    avatar_type: AvatarType
    avatars: List[dict]
    is_active: bool
    is_moderator: bool
    is_admin: bool
    joined_at: datetime
    extra: dict

    @property
    def posts_query(self) -> Query:
        return mapper_registry.query_model("Post").filter(poster_id=self.id)

    @property
    def threads_query(self) -> Query:
        return mapper_registry.query_model("Thread").filter(starter_id=self.id)

    @classmethod
    async def create(
        cls,
        name: str,
        email: str,
        *,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        group: Optional["UserGroup"] = None,
        secondary_groups: Optional[Iterable["UserGroup"]] = None,
        avatar_type: Optional[AvatarType] = None,
        avatars: Optional[List[dict]] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[Context] = None,
    ) -> "User":
        password_hash = None
        if password:
            password_hash = await hash_password(password)

        if group is None:
            group = await UserGroup.query.one(is_default=True)

        groups_ids = [group.id]
        if secondary_groups:
            groups_ids += [secondary_group.id for secondary_group in secondary_groups]
        acl_key = create_acl_key(groups_ids)

        data: Dict[str, Any] = {
            "name": name,
            "slug": slugify(name),
            "email": normalize_email(email),
            "email_hash": get_email_hash(email),
            "full_name": full_name,
            "group_id": group.id,
            "acl_key": acl_key,
            "password": password_hash,
            "avatar_type": avatar_type or AvatarType.GRAVATAR,
            "avatars": avatars or [],
            "is_active": is_active,
            "is_moderator": is_moderator,
            "is_admin": is_admin,
            "joined_at": joined_at or timezone.now(),
            "extra": extra or {},
        }

        user = await cls.query.insert(**data)

        await cls._create_group_memberships(user, group, secondary_groups or [])

        return user

    @classmethod
    async def _create_group_memberships(
        cls, user: "User", main: "UserGroup", secondary: Iterable["UserGroup"]
    ):
        all_groups = [main] + list(secondary)
        groups_ids = list({group.id for group in all_groups})
        groups_ids.sort()

        new_memberships = user_group_memberships.insert().values(
            [
                {
                    "user_id": user.id,
                    "group_id": group_id,
                    "is_main": group_id == main.id,
                }
                for group_id in groups_ids
            ]
        )
        await database.execute(new_memberships)

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

    async def update_groups(
        self, main: "UserGroup", secondary: Iterable["UserGroup"]
    ) -> "User":
        async with database.transaction():
            clear_memberships = user_group_memberships.delete().where(
                user_group_memberships.c.user_id == self.id
            )
            await database.execute(clear_memberships)

            all_groups = [main] + list(secondary)
            groups_ids = list({group.id for group in all_groups})
            groups_ids.sort()

            new_memberships = user_group_memberships.insert().values(
                [
                    {
                        "user_id": self.id,
                        "group_id": group_id,
                        "is_main": group_id == main.id,
                    }
                    for group_id in set(groups_ids)
                ]
            )
            await database.execute(new_memberships)

            changes = {
                "acl_key": create_acl_key(groups_ids),
                "group_id": main.id,
            }

            await User.query.filter(id=self.id).update(**changes)
            return self.replace(**changes)

    async def get_groups(self) -> List["UserGroup"]:
        query = (
            select(*user_groups.c.values())
            .select_from(user_group_memberships.join(user_groups))
            .where(user_group_memberships.c.user_id == self.id)
        )
        rows = await database.fetch_all(query)
        groups = [UserGroup(**row._mapping) for row in rows]
        groups.sort(key=lambda x: x.ordering)
        main_group = None
        secondary_groups = []
        for group in groups:
            if group.id == self.group_id:
                main_group = group
            else:
                secondary_groups.append(group)
        return [cast("UserGroup", main_group)] + secondary_groups


@register_model("UserGroup", user_groups)
@dataclass
class UserGroup(Model):
    id: int
    name: str
    slug: str
    title: Optional[str]
    css_suffix: Optional[str]
    ordering: int
    is_default: bool
    is_guest: bool
    is_hidden: bool
    is_moderator: bool
    is_admin: bool

    @classmethod
    async def create(
        cls,
        name: str,
        *,
        title: Optional[str] = None,
        css_suffix: Optional[str] = None,
        is_hidden: bool = False,
        is_moderator: bool = False,
        is_admin: bool = False,
        context: Optional[Context] = None,
    ) -> "UserGroup":
        last_group = (
            await UserGroup.query.limit(1).order_by("-ordering").one_flat("ordering")
        )
        ordering = last_group["ordering"] + 1

        data: Dict[str, Any] = {
            "name": name,
            "slug": slugify(name),
            "title": title or None,
            "css_suffix": css_suffix or None,
            "ordering": ordering,
            "is_default": False,
            "is_guest": False,
            "is_hidden": is_hidden,
            "is_moderator": is_moderator,
            "is_admin": is_admin,
        }

        return await cls.query.insert(**data)

    async def update(
        self,
        *,
        name: Optional[str] = None,
        is_hidden: Optional[bool] = None,
        is_moderator: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        context: Optional[Context] = None,
    ) -> "UserGroup":
        changes: Dict[str, Any] = {}

        if name is not None and name != self.name:
            changes["name"] = name
            changes["slug"] = slugify(name)

        if is_hidden is not None and is_hidden != self.is_hidden:
            changes["is_hidden"] = is_hidden
        if is_moderator is not None and is_moderator != self.is_moderator:
            changes["is_moderator"] = is_moderator
        if is_admin is not None and is_admin != self.is_admin:
            changes["is_admin"] = is_admin

        if not changes:
            return self

        await UserGroup.query.filter(id=self.id).update(**changes)

        return self.replace(**changes)
