import pytest
from django.core.exceptions import ValidationError

from ...categories.proxy import CategoriesProxy
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ..validators import validate_other_category_choices_exist


def test_validate_other_category_choices_exist_fails_if_other_accessible_categories_dont_exist(
    cache_versions, moderator, user_permissions_factory
):
    user_permissions = user_permissions_factory(moderator)
    categories = CategoriesProxy(user_permissions, cache_versions)

    with pytest.raises(ValidationError):
        validate_other_category_choices_exist(user_permissions, categories)


def test_validate_other_category_choices_exist_fails_if_other_browseable_categories_dont_exist(
    cache_versions,
    moderators_group,
    moderator,
    sibling_category,
    user_permissions_factory,
):
    CategoryGroupPermission.objects.create(
        group=moderators_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )

    user_permissions = user_permissions_factory(moderator)
    categories = CategoriesProxy(user_permissions, cache_versions)

    with pytest.raises(ValidationError):
        validate_other_category_choices_exist(user_permissions, categories)


def test_validate_other_category_choices_exist_fails_if_other_moderator_categories_dont_exist(
    cache_versions,
    members_group,
    user,
    default_category,
    sibling_category,
    user_permissions_factory,
):
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        group=members_group,
        is_global=False,
        categories=[default_category.id],
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    with pytest.raises(ValidationError):
        validate_other_category_choices_exist(user_permissions, categories)


def test_validate_other_category_choices_exist_passes_if_other_accessible_moderator_categories_exist(
    cache_versions,
    members_group,
    user,
    default_category,
    sibling_category,
    user_permissions_factory,
):
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=sibling_category,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        group=members_group,
        category=sibling_category,
        permission=CategoryPermission.BROWSE,
    )

    Moderator.objects.create(
        group=members_group,
        is_global=False,
        categories=[default_category.id, sibling_category.id],
    )

    user_permissions = user_permissions_factory(user)
    categories = CategoriesProxy(user_permissions, cache_versions)

    validate_other_category_choices_exist(user_permissions, categories)
