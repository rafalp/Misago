import pytest

from ...categories.enums import CategoryTree
from ...categories.models import Category
from ...categories.proxy import CategoriesProxy
from ...users.test import create_test_user
from ..enums import CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy
from ..threads import CategoryThreadsQuerysetFilter, ThreadsQuerysetFilter


@pytest.fixture
def threads_filter_factory(cache_versions):
    def filter_factory_function(user):
        permissions = UserPermissionsProxy(user, cache_versions)
        categories = CategoriesProxy(permissions, cache_versions)
        return ThreadsQuerysetFilter(permissions, categories.categories_list)

    return filter_factory_function


@pytest.fixture
def category_threads_filter_factory(cache_versions):
    def filter_factory_function(user, category):
        permissions = UserPermissionsProxy(user, cache_versions)
        categories = CategoriesProxy(permissions, cache_versions)
        categories_data = categories.get_category_descendants(category.id)

        return CategoryThreadsQuerysetFilter(
            permissions,
            categories.categories_list,
            current_category=categories_data[0],
            child_categories=categories_data[1:],
            include_children=category.list_children_threads,
        )

    return filter_factory_function


@pytest.fixture
def category(root_category):
    category = Category(name="Parent", slug="parent")
    category.insert_at(root_category, position="last-child", save=True)
    return category


@pytest.fixture
def child_category(category):
    child_category = Category(name="Child", slug="child")
    child_category.insert_at(category, position="last-child", save=True)
    return child_category


@pytest.fixture
def sibling_category(root_category):
    sibling_category = Category(name="Sibling", slug="sibling")
    sibling_category.insert_at(root_category, position="last-child", save=True)
    return sibling_category


@pytest.fixture
def category_guests_see_permission(category, guests_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def category_guests_browse_permission(category, guests_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def category_members_see_permission(category, members_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def category_members_browse_permission(category, members_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def category_moderators_see_permission(category, moderators_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def category_moderators_browse_permission(category, moderators_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=moderators_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def category_custom_see_permission(category, custom_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=custom_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def category_custom_browse_permission(category, custom_group):
    return CategoryGroupPermission.objects.create(
        category=category,
        group=custom_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def child_category_guests_see_permission(child_category, guests_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def child_category_guests_browse_permission(child_category, guests_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def child_category_members_see_permission(child_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def child_category_members_browse_permission(child_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def child_category_moderators_see_permission(child_category, moderators_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def child_category_moderators_browse_permission(child_category, moderators_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=moderators_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def child_category_custom_see_permission(child_category, custom_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=custom_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def child_category_custom_browse_permission(child_category, custom_group):
    return CategoryGroupPermission.objects.create(
        category=child_category,
        group=custom_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def sibling_category_guests_see_permission(sibling_category, guests_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def sibling_category_guests_browse_permission(sibling_category, guests_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def sibling_category_members_see_permission(sibling_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def sibling_category_members_browse_permission(sibling_category, members_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def sibling_category_moderators_see_permission(sibling_category, moderators_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def sibling_category_moderators_browse_permission(sibling_category, moderators_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=moderators_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def sibling_category_custom_group_see_permission(sibling_category, custom_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=custom_group,
        permission=CategoryPermission.SEE,
    )


@pytest.fixture
def sibling_category_custom_group_browse_permission(sibling_category, custom_group):
    return CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=custom_group,
        permission=CategoryPermission.BROWSE,
    )


@pytest.fixture
def category_moderator(user, user_password):
    user = create_test_user(
        "CategoryModerator", "catmoderator@example.com", user_password
    )

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=list(
            Category.objects.filter(tree_id=CategoryTree.THREADS).values_list(
                "id", flat=True
            )
        ),
    )

    return user


@pytest.fixture
def category_thread(thread_factory, category):
    return thread_factory(category, title="Category Thread")


@pytest.fixture
def category_pinned_thread(thread_factory, category):
    return thread_factory(category, title="Category Pinned Thread", weight=1)


@pytest.fixture
def category_pinned_globally_thread(thread_factory, category):
    return thread_factory(category, title="Category Global Thread", weight=2)


@pytest.fixture
def child_category_thread(thread_factory, child_category):
    return thread_factory(child_category, title="Child Thread")


@pytest.fixture
def child_category_pinned_thread(thread_factory, child_category):
    return thread_factory(child_category, title="Child Pinned Thread", weight=1)


@pytest.fixture
def child_category_pinned_globally_thread(thread_factory, child_category):
    return thread_factory(child_category, title="Child Global Thread", weight=2)


@pytest.fixture
def sibling_category_thread(thread_factory, sibling_category):
    return thread_factory(sibling_category, title="Sibling Thread")


@pytest.fixture
def sibling_category_pinned_thread(thread_factory, sibling_category):
    return thread_factory(sibling_category, title="Sibling Pinned Thread", weight=1)


@pytest.fixture
def sibling_category_pinned_globally_thread(thread_factory, sibling_category):
    return thread_factory(sibling_category, title="Sibling Global Thread", weight=2)


@pytest.fixture
def category_user_thread(thread_factory, category, user):
    return thread_factory(category, title="Category Thread", starter=user)


@pytest.fixture
def child_category_user_thread(thread_factory, child_category, user):
    return thread_factory(child_category, title="Child Thread", starter=user)


@pytest.fixture
def sibling_category_user_thread(thread_factory, sibling_category, user):
    return thread_factory(sibling_category, title="Sibling Thread", starter=user)
