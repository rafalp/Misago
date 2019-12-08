from ..database.queries import delete
from ..tables import users


async def delete_user(user_id: int):
    await delete(users, user_id)
