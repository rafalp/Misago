from ..categories.proxy import CategoriesProxy
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy


def get_searchable_category_ids(
    user_permissions: UserPermissionsProxy, categories: CategoriesProxy
) -> set[int]:
    return set(user_permissions.categories[CategoryPermission.BROWSE]).difference(
        category.id for category in categories.values() if category.is_vanilla
    )
