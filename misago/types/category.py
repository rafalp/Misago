from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    id: int
    type: int
    name: str
    slug: str
    extra: dict
    left: int = 0
    right: int = 0
    depth: int = 0
    threads: int = 0
    posts: int = 0
    parent_id: Optional[int] = None
    is_closed: Optional[bool] = False

    def has_children(self) -> bool:
        return (self.left + 1) < self.right

    def is_parent(self, node: "MPTTNode") -> bool:
        return self.left < node.left and self.right > node.right

    def is_child(self, node: "MPTTNode") -> bool:
        return self.left > node.left and self.right < node.right
