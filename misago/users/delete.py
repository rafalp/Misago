from ..database.queries import delete
from ..tables import users
from ..threads.delete import delete_user_posts, delete_user_threads
from ..types import User


async def delete_user_content(user: User):
    await delete_user_threads(user)
    await delete_user_posts(user)


async def delete_user(user: User):
    await delete(users, user.id)
