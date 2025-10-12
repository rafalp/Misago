from django.urls import reverse

from ...categories.enums import CategoryChildrenComponent
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains, assert_not_contains


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_returns_redirect_to_site_index_if_accessed_through_url(
    moderator_client,
):
    response = moderator_client.get(reverse("misago:thread-list"))
    assert response.status_code == 302
    assert response["location"] == reverse("misago:index")


@override_dynamic_settings(
    index_view="categories",
    threads_list_categories_component=CategoryChildrenComponent.DISABLED,
)
def test_thread_list_view_renders_no_subcategories_component(default_category, client):
    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, "list-group-category")


@override_dynamic_settings(
    index_view="categories",
    threads_list_categories_component=CategoryChildrenComponent.FULL,
)
def test_thread_list_view_renders_full_subcategories_component(
    default_category, client
):
    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, default_category.name)
    assert_contains(response, "list-group-category")


@override_dynamic_settings(
    index_view="categories",
    threads_list_categories_component=CategoryChildrenComponent.DROPDOWN,
)
def test_thread_list_view_renders_dropdown_subcategories_component(
    default_category, client, guests_group
):
    default_category.children_categories_component = CategoryChildrenComponent.DROPDOWN
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )

    response = client.get(default_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "dropdown-category")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_guests(db, client):
    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_category_moderators(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_global_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_guests_in_htmx(db, client):
    response = client.get(reverse("misago:thread-list"), headers={"hx-request": "true"})
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_users_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:thread-list"), headers={"hx-request": "true"}
    )
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_category_moderators_in_htmx(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.get(
        reverse("misago:thread-list"), headers={"hx-request": "true"}
    )
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_empty_to_global_moderators_in_htmx(moderator_client):
    response = moderator_client.get(
        reverse("misago:thread-list"), headers={"hx-request": "true"}
    )
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_guests(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_category_moderators(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.get(reverse("misago:index"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_global_moderators(
    moderator_client,
):
    response = moderator_client.get(reverse("misago:index"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_guests_in_htmx(db, client):
    response = client.get(reverse("misago:index"), headers={"hx-request": "true"})
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_users_in_htmx(user_client):
    response = user_client.get(reverse("misago:index"), headers={"hx-request": "true"})
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_category_moderators_in_htmx(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.get(reverse("misago:index"), headers={"hx-request": "true"})
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_renders_empty_to_global_moderators_in_htmx(
    moderator_client,
):
    response = moderator_client.get(
        reverse("misago:index"), headers={"hx-request": "true"}
    )
    assert_contains(response, "No threads have been started yet")
