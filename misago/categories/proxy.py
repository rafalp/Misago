from functools import cached_property

from ..permissions.proxy import UserPermissionsProxy
from .categories import get_categories


class CategoriesProxy:
    user_permissions: UserPermissionsProxy
    cache_versions: dict

    def __init__(self, user_permissions: UserPermissionsProxy, cache_versions: dict):
        self.user_permissions = user_permissions
        self.cache_versions = cache_versions

    @cached_property
    def categories(self) -> dict[int, dict]:
        return get_categories(self.user_permissions, self.cache_versions)

    @cached_property
    def categories_list(self) -> list[dict]:
        return list(self.categories.values())

    @cached_property
    def top_categories_list(self) -> list[dict]:
        return [
            category for category in self.categories_list if not category["parent_id"]
        ]

    def get_category_parents(
        self, category_id: int, include_self: bool = True
    ) -> list[dict]:
        parents: list[dict] = []

        category = self.categories[category_id]
        while category["level"]:
            if category["id"] != category_id or include_self:
                parents.append(category)
            if category["parent_id"]:
                category = self.categories[category["parent_id"]]

        return parents

    def get_category_path(
        self, category_id: int, include_self: bool = True
    ) -> list[dict]:
        parents = self.get_category_parents(category_id, include_self)
        return reversed(parents)

    def get_category_children(self, category_id: int) -> list[dict]:
        children: list[dict] = []

        for category in self.categories_list:
            if category["parent_id"] == category_id:
                children.append(category)

        return children
