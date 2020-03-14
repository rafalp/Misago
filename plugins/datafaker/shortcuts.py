import random
from typing import Optional, Tuple

from faker import Faker
from misago.types import User

from .randomrow import get_random_user
from .users import get_fake_username


async def get_random_poster(fake: Faker) -> Tuple[Optional[User], Optional[str]]:
    if random.randint(0, 100) > 80:
        return None, get_fake_username(fake)

    poster = await get_random_user()
    poster_name = None
    if not poster:
        poster_name = get_fake_username(fake)

    return poster, poster_name
