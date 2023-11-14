import hashlib


def hash_email(email: str) -> str:
    return hashlib.md5(email.lower().encode()).hexdigest()


def slugify_username(username: str) -> str:
    return username.lower().strip().replace("_", "-")
