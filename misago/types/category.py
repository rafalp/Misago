from dataclasses import dataclass
from typing import Optional

from .mptt import MPTTNode


@dataclass
class Category(MPTTNode):
    id: int
    type: int
    name: str
    slug: str
    extra: dict
    left: int = 0
    right: int = 0
    depth: int = 0
    parent_id: Optional[int] = None
    is_closed: Optional[bool] = False
