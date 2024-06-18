from collections import defaultdict
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
        top_categories: list[dict] = []
        children: dict[int, list[dict]] = defaultdict(list)

        for item in self.categories_list:
            category = item.copy()

            if category["parent_id"] is None:
                children[item["id"]] = []
                top_categories.append(category)

            elif category["parent_id"] in children:
                children[category["parent_id"]].append(category)

        # Flatten menu for React.js
        menu_items: list[dict] = []
        for category in top_categories:
            category_children = children.get(category["id"])
            if not category["is_vanilla"] or category_children:
                menu_items.append(category)
                if category_children:
                    menu_items += category_children
                    menu_items[-1]["last"] = True

        if menu_items:
            menu_items[-1].pop("last", None)

        return menu_items

    def get_category_parents(
        self, category_id: int, include_self: bool = True
    ) -> list[dict]:
        parents: list[dict] = []

        category = self.categories[category_id]
        while True:
            if category["id"] != category_id or include_self:
                parents.append(category)
            if not category["parent_id"]:
                break
            category = self.categories[category["parent_id"]]

        return parents

    def get_category_path(
        self, category_id: int, include_self: bool = True
    ) -> list[dict]:
        parents = self.get_category_parents(category_id, include_self)
        return list(reversed(parents))
