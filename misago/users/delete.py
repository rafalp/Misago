from typing import Awaitable

from ..threads.delete import delete_user_posts, delete_user_threads
from .hooks import delete_user_content_hook, delete_user_hook
from .models import User


def delete_user_content(user: User) -> Awaitable[User]:
    return delete_user_content_hook.call_action(delete_user_content_action, user)


async def delete_user_content_action(user: User):
    await delete_user_threads(user)
    await delete_user_posts(user)


async def delete_user(user: User):
    async def action(user):
        await user.delete()

    await delete_user_hook.call_action(action, user)
