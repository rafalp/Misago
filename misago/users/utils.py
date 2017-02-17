import hashlib


def hash_email(email):
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()
