from hashlib import md5


def hash_trigger(message):
    return md5(message).hexdigest()[:8]


def variables_dict(plain=None, links=None, users=None, threads=None):
    final_variables = {}

    final_variables.update(plain)

    return final_variables
