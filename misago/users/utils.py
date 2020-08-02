import hashlib
import uuid


def hash_email(email):
    return hashlib.md5(email.lower().encode("utf-8")).hexdigest()


def suffix_taken_username():
    return str(uuid.uuid4()).split("-", 1)[0]
