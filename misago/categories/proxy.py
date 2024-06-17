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

    def get_categories_menu(self) -> list[dict]:
        top_categories: dict[int, dict] = {}
        for item in self.categories_list:
            category = item.copy()
            category["children"] = []

            if category["parent_id"] is None:
                top_categories[category["id"]] = category
            elif category["parent_id"] in top_categories:
                parent_category = top_categories[category["parent_id"]]
                parent_category["children"].append(category)

        # Flatten menu for React.js
        menu_items: list[dict] = []
        for category in top_categories.values():
            if not category["is_vanilla"] or category["children"]:
                children = category.pop("children")
                menu_items.append(category)
                menu_items += children
                if children:
                    menu_items[-1]["last"] = True

        menu_items[-1].pop("last", None)

        return menu_items

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
