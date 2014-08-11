from hashlib import md5


def target_trigger(message, obj_id=None):
    hash_seed = [message]

    if obj_pk:
      hash_seed.append(unicode(obj_id))

    return md5(hash_seed.join('+')).hexdigest[:8]


def variables_dict(plain=None, links=None, users=None, threads=None):
    final_variables = {}

    final_variables.update(plain)

    return final_variables
