from dataclasses import dataclass


@dataclass(frozen=True)
class ModeratorData:
    is_global: bool
    categories_ids: set[int]
