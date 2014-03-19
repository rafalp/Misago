import hashlib


def hash_email(email):
    email = email.lower()
    while len(email) < 15:
        email *= 2
    return hashlib.sha256(email).hexdigest()
