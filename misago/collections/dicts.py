from typing import Any


def set_key_before(src: dict, before: Any, key: Any, value: Any) -> dict:
    if before not in src:
        raise KeyError(before)

    new_dict = {}
    for src_key, src_value in src.items():
        if src_key == before:
            new_dict[key] = value
        new_dict[src_key] = src_value

    return new_dict


def set_key_after(src: dict, after: Any, key: Any, value: Any) -> dict:
    if after not in src:
        raise KeyError(after)

    new_dict = {}
    for src_key, src_value in src.items():
        new_dict[src_key] = src_value
        if src_key == after:
            new_dict[key] = value

    return new_dict
