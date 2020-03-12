import random

from faker import Faker
from misago.types import User
from misago.users.create import create_user
from misago.utils.strings import get_random_string


PASSWORD = "password"


def create_fake_user(fake: Faker) -> User:
    return create_user(get_fake_username(fake), email=fake.email(), password=PASSWORD,)


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
