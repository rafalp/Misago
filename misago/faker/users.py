import hashlib
import random

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from ..users.bans import ban_user
from ..users.test import create_test_user
from .utils import retry_on_db_error

User = get_user_model()

AVATAR_SIZES = (400, 200, 100)
GRAVATAR_URL = "https://www.gravatar.com/avatar/%s?s=%s&d=retro"
PASSWORD = "password"


@retry_on_db_error
def get_fake_user(fake, rank=None, requires_activation=User.ACTIVATION_NONE):
    username = get_fake_username(fake)
    email = fake.email()
    return create_test_user(
        username,
        email.lower(),
        PASSWORD,
        avatars=get_fake_avatars(email),
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


def get_fake_deleted_user(fake, rank=None):
    user = get_fake_user(fake, rank=rank)
    user.is_active = False
    user.save(update_fields=["is_active"])
    return user


def get_fake_username(fake):
    possible_usernames = [
        fake.first_name(),
        fake.last_name(),
        fake.name().replace(" ", ""),
        fake.user_name(),
        get_random_string(random.randint(4, 8)),
    ]

    return random.choice(possible_usernames)


def get_fake_avatars(email):
    email_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()

    return [
        {"size": size, "url": GRAVATAR_URL % (email_hash, size)}
        for size in AVATAR_SIZES
    ]
