import hashlib

HASH_LENGTH = 8


def get_file_hash(file):
    if not file.size:
        return "0" * HASH_LENGTH
    file_hash = hashlib.md5()
    for chunk in file.chunks():
        file_hash.update(chunk)
    return file_hash.hexdigest()[:HASH_LENGTH]
