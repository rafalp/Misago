import hashlib
import uuid


def hash_email(email):
    return hashlib.md5(email.lower().encode("utf-8")).hexdigest()


def gen_suffix_username():
    return str(uuid.uuid4()).split("-", 1)[0]
