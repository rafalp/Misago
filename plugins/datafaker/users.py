import random
from datetime import datetime
from typing import Optional

from asyncpg.exceptions import UniqueViolationError
from faker import Faker

from misago.users.create import create_user
from misago.users.models import User
from misago.utils.strings import get_random_string


PASSWORD = "password"


async def create_fake_user(
    fake: Faker, *, joined_at: Optional[datetime] = None
) -> User:
    user = None
    while not user:
        try:
            user = await create_user(
                get_fake_username(fake),
                email=fake.email(),
                password=PASSWORD,
                joined_at=joined_at,
            )
        except UniqueViolationError:
            pass

    return user


def get_fake_username(fake: Faker) -> str:
    possible_usernames = [
        fake.first_name(),
        fake.last_name(),
        fake.name().replace(" ", ""),
        fake.user_name(),
        fake.domain_word(),
        get_random_string(random.randint(2, 8)),
    ]

    username = random.choice(possible_usernames)
    username += get_random_string(random.randint(2, 8))

    return username
