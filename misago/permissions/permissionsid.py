from hashlib import md5


def get_permissions_id(groups_ids: list[int]):
    return md5((".".join(map(str, groups_ids))).encode()).hexdigest()[:12]
