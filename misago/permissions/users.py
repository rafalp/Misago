from ..context import Context
from ..users.models import User
from .permissions import CorePermission
from .groups import get_groups_permissions


async def get_user_permissions(context: Context, user: User) -> dict:
    user_groups = await user.get_groups()
    permissions = await get_groups_permissions(user_groups)

    if user.is_moderator and CorePermission.MODERATOR not in permissions["core"]:
        permissions["core"].append(CorePermission.MODERATOR)

    if user.is_admin and CorePermission.ADMIN not in permissions["core"]:
        permissions["core"].append(CorePermission.ADMIN)

    return permissions
