from passlib.hash import django_pbkdf2_sha256, pbkdf2_sha256, plaintext

from ..conf import settings
from .hasher import PasswordHasher

__all__ = [
    "password_hasher",
    "hash_password",
    "check_password",
    "is_password_outdated",
]


if settings.test:
    # Use plaintext to keep tests suite fast
    password_hasher = PasswordHasher([plaintext])
else:
    password_hasher = PasswordHasher([pbkdf2_sha256, django_pbkdf2_sha256])


hash_password = password_hasher.hash_password
check_password = password_hasher.check_password
is_password_outdated = password_hasher.is_password_outdated
