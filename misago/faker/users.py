import random

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from ..users.bans import ban_user
from ..users.test import create_test_user
from .utils import retry_on_db_error

User = get_user_model()

PASSWORD = "password"


@retry_on_db_error
def get_fake_user(fake, rank=None, requires_activation=User.ACTIVATION_NONE):
    username = get_fake_username(fake)
    return create_test_user(
        username,
        fake.email(),
        PASSWORD,
        rank=rank,
        requires_activation=requires_activation,
    )


def get_fake_banned_user(fake, rank=None):
    user = get_fake_user(fake, rank=rank)
    ban_user(user)
    return user


def get_fake_inactive_user(fake, rank=None):
    return get_fake_user(fake, rank=rank, requires_activation=User.ACTIVATION_USER)


def get_fake_admin_activated_user(fake, rank=None):
    return get_fake_user(fake, rank=rank, requires_activation=User.ACTIVATION_ADMIN)


def get_fake_username(fake):
    possible_usernames = [
        fake.first_name(),
        fake.last_name(),
        fake.name().replace(" ", ""),
        fake.user_name(),
        get_random_string(random.randint(4, 8)),
    ]

    return random.choice(possible_usernames)
