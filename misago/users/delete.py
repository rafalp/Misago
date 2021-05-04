from ..threads.delete import delete_user_posts, delete_user_threads
from .models import User


async def delete_user_content(user: User):
    await delete_user_threads(user)
    await delete_user_posts(user)
