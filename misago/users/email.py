from hashlib import md5


def normalize_email(email: str) -> str:
    name, domain = email.rsplit("@", 1)
    return f"{name}@{domain.lower()}"


def get_email_hash(email: str) -> str:
    return md5(email.lower().encode("ascii")).hexdigest()
