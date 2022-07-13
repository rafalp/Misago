from hashlib import md5
from typing import Iterable


def create_acl_key(groups_ids: Iterable[int]) -> str:
    groups_ids = sorted(set(groups_ids))
    groups_ids_str = "_".join(map(str, groups_ids))
    return md5(groups_ids_str.encode()).hexdigest()[:16]
