import random

from django.utils.crypto import get_random_string
from faker import Factory


def get_fake_username(fake):
    possible_usernames = [
        fake.first_name(),
        fake.last_name(),
        fake.name().replace(" ", ""),
        fake.user_name(),
        get_random_string(random.randint(4, 8)),
    ]

    return random.choice(possible_usernames)
