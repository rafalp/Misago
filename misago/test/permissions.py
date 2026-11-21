from ..categories.models import Category
from ..permissions.enums import CategoryPermission
from ..permissions.models import CategoryGroupPermission
from ..users.models import Group


def grant_user_group_category_permissions(
    user_group: Group, category: Category, *permissions: CategoryPermission
):
    CategoryGroupPermission.objects.bulk_create(
        [
            CategoryGroupPermission(
                category=category,
                group=user_group,
                permission=permission,
            )
            for permission in permissions
        ]
    )


def remove_user_group_category_permissions(user_group: Group, category: Category):
    CategoryGroupPermission.objects.filter(
        category=category,
        group=user_group,
    ).delete()


def grant_user_group_all_category_permissions(user_group: Group, category: Category):
    grant_user_group_category_permissions(
        user_group,
        category,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
        CategoryPermission.REPLY,
        CategoryPermission.ATTACHMENTS,
    )


def grant_user_group_see_category_permissions(user_group: Group, category: Category):
    grant_user_group_category_permissions(
        user_group,
        category,
        CategoryPermission.SEE,
    )


def grant_user_group_see_browse_category_permissions(
    user_group: Group, category: Category
):
    grant_user_group_category_permissions(
        user_group,
        category,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
    )
