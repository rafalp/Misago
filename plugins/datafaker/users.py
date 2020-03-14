import random
from datetime import datetime
from typing import Optional

from faker import Faker

from misago.types import User
from misago.users.create import create_user
from misago.utils.strings import get_random_string


PASSWORD = "password"


async def create_fake_user(
    fake: Faker, *, joined_at: Optional[datetime] = None
) -> User:
    return await create_user(
        get_fake_username(fake),
        email=fake.email(),
        password=PASSWORD,
        joined_at=joined_at,
    )


def get_fake_username(fake: Faker) -> str:
    possible_usernames = [
        fake.first_name(),
        fake.last_name(),
        fake.name().replace(" ", ""),
        fake.user_name(),
        fake.domain_word(),
        get_random_string(random.randint(4, 8)),
    ]

    username = random.choice(possible_usernames)
    username += get_random_string(random.randint(1, 5))

    return username
