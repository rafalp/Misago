from unittest.mock import patch

from django.urls import reverse

from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_empty_to_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, "No threads have been started yet")


def test_category_threads_list_renders_empty_to_guests(default_category, client):
    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_threads_list_renders_empty_to_users(default_category, user_client):
    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_threads_list_renders_empty_to_moderators(
    default_category, moderator_client
):
    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_child_category_threads_list_renders_empty_to_guests(child_category, client):
    response = client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_child_category_threads_list_renders_empty_to_users(
    child_category, user_client
):
    response = user_client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_child_category_threads_list_renders_empty_to_moderators(
    child_category, moderator_client
):
    response = moderator_client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_hidden_category_threads_list_renders_error_to_guests(hidden_category, client):
    response = client.get(hidden_category.get_absolute_url())
    assert response.status_code == 404


def test_hidden_category_threads_list_renders_error_to_users(
    hidden_category, user_client
):
    response = user_client.get(hidden_category.get_absolute_url())
    assert response.status_code == 404


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_to_user(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_to_anonymous_user(
    thread_factory, default_category, client
):
    thread = thread_factory(default_category)
    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


def test_category_threads_list_displays_thread_to_user(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


def test_category_threads_list_displays_thread_to_anonymous_user(
    thread_factory, default_category, client
):
    thread = thread_factory(default_category)
    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


def test_category_threads_list_displays_user_thread_to_user(
    thread_factory, default_category, user_client, other_user
):
    thread = thread_factory(default_category, starter=other_user)
    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


def test_category_threads_list_displays_user_thread_to_anonymous_user(
    thread_factory, default_category, client, other_user
):
    thread = thread_factory(default_category, starter=other_user)
    response = client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


def test_category_threads_list_includes_child_category_thread(
    thread_factory, default_category, user, user_client, other_user
):
    default_category.list_children_threads = True
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    thread = thread_factory(child_category, starter=other_user)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.BROWSE,
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)


def test_category_threads_list_excludes_child_category_thread_if_list_children_threads_is_false(
    thread_factory, default_category, user, user_client, other_user
):
    default_category.list_children_threads = False
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    thread = thread_factory(child_category, starter=other_user)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=child_category,
        group=user.group,
        permission=CategoryPermission.BROWSE,
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, "No threads have been started in this category yet")
    assert_not_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_empty_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:thread-list"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_in_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        reverse("misago:thread-list"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)


def test_category_threads_list_displays_empty_in_htmx(default_category, user_client):
    response = user_client.get(
        default_category.get_absolute_url(),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")


def test_category_threads_list_displays_thread_in_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        default_category.get_absolute_url(),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_with_animation_in_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        reverse("misago:thread-list") + "?animate_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-animate")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_without_animation_in_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        reverse("misago:thread-list") + f"?animate_new={thread.last_post_id + 1}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_without_animation_without_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        reverse("misago:thread-list") + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


def test_category_threads_list_displays_thread_with_animation_in_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        default_category.get_absolute_url() + "?animate_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-animate")


def test_category_threads_list_displays_thread_without_animation_in_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        default_category.get_absolute_url() + f"?animate_new={thread.last_post_id + 1}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


def test_category_threads_list_displays_thread_without_animation_without_htmx(
    thread_factory, default_category, user_client
):
    thread = thread_factory(default_category)
    response = user_client.get(
        default_category.get_absolute_url() + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


@override_dynamic_settings(index_view="categories")
def test_threads_list_raises_404_error_if_filter_is_invalid(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    response = user_client.get(
        reverse("misago:thread-list", kwargs={"filter": "invalid"})
    )
    assert response.status_code == 404


@override_dynamic_settings(index_view="categories")
def test_threads_list_filters_threads(
    thread_factory, default_category, user, user_client
):
    visible_thread = thread_factory(default_category, starter=user)
    hidden_thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list", kwargs={"filter": "my"}))
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@override_dynamic_settings(index_view="threads")
def test_index_threads_list_filters_threads(
    thread_factory, default_category, user, user_client
):
    visible_thread = thread_factory(default_category, starter=user)
    hidden_thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list", kwargs={"filter": "my"}))
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@override_dynamic_settings(index_view="categories")
def test_threads_list_builds_valid_filters_urls(user_client):
    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, reverse("misago:thread-list", kwargs={"filter": "my"}))


@override_dynamic_settings(index_view="threads")
def test_index_threads_list_builds_valid_filters_urls(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, reverse("misago:thread-list", kwargs={"filter": "my"}))


def test_category_threads_list_raises_404_error_if_filter_is_invalid(
    thread_factory, default_category, user, user_client
):
    thread_factory(default_category, starter=user)
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
                "filter": "invalid",
            },
        )
    )
    assert response.status_code == 404


def test_category_threads_list_filters_threads(
    thread_factory, default_category, user, user_client
):
    visible_thread = thread_factory(default_category, starter=user)
    hidden_thread = thread_factory(default_category)

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": default_category.slug,
                "filter": "my",
            },
        )
    )
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@override_dynamic_settings(index_view="categories")
@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
def test_site_threads_list_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, db, client
):
    response = client.get(reverse("misago:thread-list"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list") + "?cursor=10"

    mock_pagination.assert_called_once()


@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
def test_category_threads_list_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, default_category, client
):
    response = client.get(default_category.get_absolute_url())

    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url() + "?cursor=10"

    mock_pagination.assert_called_once()


def test_category_threads_list_returns_404_for_top_level_vanilla_category_without_children(
    default_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 404


def test_category_threads_list_returns_404_for_top_level_vanilla_category_with_invisible_children(
    default_category, child_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    CategoryGroupPermission.objects.filter(category=child_category).delete()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 404


def test_category_threads_list_renders_for_top_level_vanilla_category_with_children(
    default_category, child_category, client
):
    default_category.is_vanilla = True
    default_category.list_children_threads = False
    default_category.save()

    response = client.get(default_category.get_absolute_url())
    assert response.status_code == 200


def test_category_threads_list_renders_for_nested_vanilla_category_without_children(
    child_category, client
):
    child_category.is_vanilla = True
    child_category.list_children_threads = False
    child_category.save()

    response = client.get(child_category.get_absolute_url())
    assert response.status_code == 200


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_unread_thread(
    thread_factory, user, user_client, default_category
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)


def test_category_threads_list_renders_unread_thread(
    thread_factory, user, user_client, default_category
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)
