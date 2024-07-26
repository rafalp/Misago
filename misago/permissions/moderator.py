from dataclasses import dataclass


@dataclass(frozen=True)
class ModeratorPermissions:
    is_global: bool
    categories_ids: set[int]
    private_threads: bool
