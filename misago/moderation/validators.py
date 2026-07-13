from django.core.exceptions import ValidationError
from django.utils.translation import pgettext

from ..categories.proxy import CategoriesProxy
from ..permissions.enums import CategoryPermission
from ..permissions.proxy import UserPermissionsProxy
from .forms import get_invalid_category_choices


def validate_other_category_choices_exist(
    user_permissions: UserPermissionsProxy,
    categories: CategoriesProxy,
    message: str | None = None,
):
    invalid_category_choices = get_invalid_category_choices(
        user_permissions, categories
    )

    valid_categories = set(user_permissions.categories[CategoryPermission.BROWSE])
    valid_categories.difference_update(invalid_category_choices)

    if len(valid_categories) < 2:
        raise ValidationError(message)
