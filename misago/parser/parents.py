from typing import Iterable


def has_invalid_parent(
    invalid_parents: set[str] | None, parents: Iterable[str]
) -> bool:
    if invalid_parents and invalid_parents.intersection(parents):
        return True

    return False
