import hashlib


def get_file_hash(file):
    if file.size is None:
        return "00000000"
    file_hash = hashlib.md5()
    for chunk in file.chunks():
        file_hash.update(chunk)
    return file_hash.hexdigest()[:8]
