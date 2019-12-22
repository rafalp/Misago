from ..database.queries import delete
from ..tables import users
from ..types import User


async def delete_user(user: User):
    await delete(users, user.id)
