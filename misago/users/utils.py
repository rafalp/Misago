import hashlib


def hash_email(email: str) -> str:
    return hashlib.md5(email.lower().encode("utf-8")).hexdigest()


def slugify_username(username: str) -> str:
    return username.lower().strip().replace("_", "-")
