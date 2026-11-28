from ..categories.models import Category
from ..permissions.enums import CategoryPermission
from ..permissions.models import CategoryGroupPermission
from ..users.models import Group


def grant_category_group_permissions(
    category: Category, user_group: Group, *permissions: CategoryPermission
):
    CategoryGroupPermission.objects.bulk_create(
        [
            CategoryGroupPermission(
                category=category, group=user_group, permission=permission
            )
            for permission in permissions
        ]
    )


def remove_category_group_permissions(category: Category, user_group: Group):
    CategoryGroupPermission.objects.filter(category=category, group=user_group).delete()


def grant_group_all_category_permissions(user_group: Group, category: Category):
    grant_category_group_permissions(
        category,
        user_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
        CategoryPermission.REPLY,
        CategoryPermission.ATTACHMENTS,
    )


def grant_group_see_browse_category_permissions(user_group: Group, category: Category):
    grant_category_group_permissions(
        category,
        user_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )
