from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    id: int
    type: int
    depth: int
    left: int
    right: int
    name: str
    slug: str
    parent_id: Optional[int] = None

    def is_parent(self, category: "Category") -> bool:
        return self.left < category.left and self.right > category.right

    def is_child(self, category: "Category") -> bool:
        return self.left > category.left and self.right < category.right
