from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView
from dataclasses import dataclass, replace
from functools import cached_property
from typing import Union

from ..permissions.proxy import UserPermissionsProxy
from .categoriesdata import get_categories_data
from .models import Category


@dataclass(frozen=True)
class CategoryProxy:
    id: int
    parent_id: int | None
    level: int
    lft: int
    rght: int
    name: str
    slug: str
    short_name: str
    color: str
    css_class: str
    delay_browse_check: bool
    show_started_only: bool
    is_vanilla: bool
    plugin_data: dict

    @property
    def is_top_level(self) -> bool:
        return not self.level

    @property
    def is_leaf(self) -> bool:
        return self.lft + 1 == self.rght

    @property
    def has_children(self) -> bool:
        return self.lft + 1 < self.rght

    def is_parent(self, category: Union[Category, "CategoryProxy"]) -> bool:
        return self.id == category.parent_id

    def is_child(self, category: Union[Category, "CategoryProxy"]) -> bool:
        return self.parent_id == category.id

    def is_ancestor(self, category: Union[Category, "CategoryProxy"]) -> bool:
        return self.lft < category.lft and self.rght > category.rght

    def is_descendant(self, category: Union[Category, "CategoryProxy"]) -> bool:
        return self.lft > category.lft and self.rght < category.rght

    def replace(self, **kwargs):
        return replace(self, **kwargs)


class CategoriesProxy(Mapping[int, CategoryProxy]):
    user_permissions: UserPermissionsProxy
    cache_versions: dict[str, str]

    def __init__(
        self, user_permissions: UserPermissionsProxy, cache_versions: dict[str, str]
    ):
        self.user_permissions = user_permissions
        self.cache_versions = cache_versions

    @cached_property
    def _data(self) -> dict[int, CategoryProxy]:
        categories = get_categories_data(self.user_permissions, self.cache_versions)

        return {
            category_id: CategoryProxy(**category)
            for category_id, category in categories.items()
        }

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, category: Category | CategoryProxy | int) -> bool:
        category_id = category if isinstance(category, int) else category.id
        return category_id in self._data

    def __getitem__(self, category_id: int) -> CategoryProxy:
        return self._data[category_id]

    def __iter__(self) -> Iterator[int]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def keys(self) -> KeysView[int]:
        return self._data.keys()

    def values(self) -> ValuesView[CategoryProxy]:
        return self._data.values()

    def items(self) -> ItemsView[int, CategoryProxy]:
        return self._data.items()

    def get(self, category_id: int) -> CategoryProxy | None:
        return self._data.get(category_id)

    def get_parent(
        self, category: Category | CategoryProxy | int
    ) -> CategoryProxy | None:
        category_id = category if isinstance(category, int) else category.id
        category_obj = self[category_id]

        if category_obj.parent_id is not None:
            return self.get(category_obj.parent_id)

        return None

    def get_children(
        self, category: Category | CategoryProxy | int, include_self: bool = False
    ) -> list[CategoryProxy]:
        category_id = category if isinstance(category, int) else category.id

        return [
            item
            for item in self.values()
            if item.parent_id == category_id
            or (include_self and item.id == category_id)
        ]

    def get_ancestors(
        self, category: Category | CategoryProxy | int, include_self: bool = False
    ) -> list[CategoryProxy]:
        category_id = category if isinstance(category, int) else category.id
        category_obj = self[category_id]

        return [
            item
            for item in self.values()
            if item.is_ancestor(category_obj)
            or (include_self and item.id == category_obj.id)
        ]

    def get_descendants(
        self, category: Category | CategoryProxy | int, include_self: bool = False
    ) -> list[CategoryProxy]:
        category_id = category if isinstance(category, int) else category.id
        category_obj = self[category_id]

        return [
            item
            for item in self.values()
            if item.is_descendant(category_obj)
            or (include_self and item.id == category_obj.id)
        ]
