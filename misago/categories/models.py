from dataclasses import dataclass
from typing import Any, Awaitable, Dict, Optional, Union

from ..database import MapperQuery, Model, model_registry, register_model
from ..graphql import GraphQLContext
from ..tables import categories
from ..utils.strings import slugify
from .categorytypes import CategoryTypes


@register_model("Category", categories)
@dataclass
class Category(Model):
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

    @classmethod
    def create(
        cls,
        name: str,
        *,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        parent: Optional["Category"] = None,
        left: Optional[int] = 0,
        right: Optional[int] = 0,
        depth: Optional[int] = 0,
        threads: Optional[int] = 0,
        posts: Optional[int] = 0,
        is_closed: Optional[bool] = False,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable["Category"]:
        data: Dict[str, Any] = {
            "type": CategoryTypes.THREADS,
            "name": name,
            "slug": slugify(name),
            "color": (color or "#00FF00").upper(),
            "icon": icon or None,
            "parent_id": parent.id if parent else None,
            "left": left,
            "right": right,
            "depth": depth,
            "threads": threads,
            "posts": posts,
            "is_closed": is_closed or False,
            "extra": extra or {},
        }

        return cls.query.insert(**data)

    async def update(
        self,
        *,
        name: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        parent: Optional[Union["Category", bool]] = None,
        left: Optional[int] = None,
        right: Optional[int] = None,
        depth: Optional[int] = None,
        threads: Optional[int] = None,
        increment_threads: Optional[bool] = False,
        posts: Optional[int] = None,
        increment_posts: Optional[bool] = False,
        is_closed: Optional[bool] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> "Category":
        changes: Dict[str, Any] = {}

        if name is not None and name != self.name:
            changes["name"] = name
            changes["slug"] = slugify(name)

        if color is not None and color != self.color:
            changes["color"] = color.upper()

        if icon is not None and icon != self.icon:
            changes["icon"] = icon or None

        if parent is True:
            raise ValueError("'parent' must be of type 'None', 'False' or 'Category'")

        if parent and isinstance(parent, Category):
            if parent.id == self.id:
                raise ValueError("category can't be its own parent")
            if parent.id != self.parent_id:
                changes["parent_id"] = parent.id
        elif parent is False and self.parent_id:
            changes["parent_id"] = None

        if left is not None and left != self.left:
            changes["left"] = left
        if right is not None and right != self.right:
            changes["right"] = right
        if depth is not None and depth != self.depth:
            changes["depth"] = depth

        if threads is not None and increment_threads:
            raise ValueError(
                "'threads' and 'increment_threads' options are mutually exclusive"
            )
        if threads is not None and threads != self.threads:
            changes["threads"] = threads
        if increment_threads:
            changes["threads"] = categories.c.threads + 1

        if posts is not None and increment_posts:
            raise ValueError(
                "'posts' and 'increment_posts' options are mutually exclusive"
            )
        if posts is not None and posts != self.posts:
            changes["posts"] = posts
        if increment_posts:
            changes["posts"] = categories.c.posts + 1

        if is_closed is not None and is_closed != self.is_closed:
            changes["is_closed"] = is_closed

        if extra is not None and extra != self.extra:
            changes["extra"] = extra

        if not changes:
            return self

        await Category.query.filter(id=self.id).update(**changes)

        # replace SQL expressions with actual ints for use in new dataclass
        if increment_threads:
            changes["threads"] = self.threads + 1
        if increment_posts:
            changes["posts"] = self.posts + 1

        return self.replace(**changes)

    def delete(self):
        return Category.query.filter(id=self.id).delete()

    def __str__(self):
        return self.name

    def has_children(self) -> bool:
        return (self.left + 1) < self.right

    def is_parent(self, category: "Category") -> bool:
        return self.left < category.left and self.right > category.right

    def is_child(self, category: "Category") -> bool:
        return self.left > category.left and self.right < category.right
