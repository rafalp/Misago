from dataclasses import dataclass
from typing import Optional

from ..database import MapperQuery, model_registry


@dataclass
class Category:
    id: int
    type: int
    name: str
    slug: str
    color: str
    extra: dict
    left: int = 0
    right: int = 0
    depth: int = 0
    threads: int = 0
    posts: int = 0
    parent_id: Optional[int] = None
    icon: Optional[str] = None
    is_closed: Optional[bool] = False

    @property
    def posts_query(self) -> MapperQuery:
        return model_registry["Post"].filter(category_id=self.id)

    @property
    def threads_query(self) -> MapperQuery:
        return model_registry["Thread"].filter(category_id=self.id)

    def __str__(self):
        return self.name

    def has_children(self) -> bool:
        return (self.left + 1) < self.right

    def is_parent(self, category: "Category") -> bool:
        return self.left < category.left and self.right > category.right

    def is_child(self, category: "Category") -> bool:
        return self.left > category.left and self.right < category.right
