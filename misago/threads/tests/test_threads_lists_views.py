from unittest.mock import patch

from django.urls import reverse

from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..models import ThreadParticipant
from ..test import post_thread


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_empty_to_guests(db, client):
    response = client.get(reverse("misago:threads"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, "No threads have been started yet")


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_empty_to_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:threads"))
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


def test_private_threads_list_shows_permission_error_to_guests(db, client):
    response = client.get(reverse("misago:private-threads"))
    assert_contains(
        response, "You must be signed in to use private threads.", status_code=403
    )


def test_private_threads_list_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Private threads")
    assert_contains(response, "You aren't participating in any private threads")


def test_private_threads_list_shows_permission_error_to_users_without_permission(
    user_client, members_group
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(reverse("misago:private-threads"))
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_threads_list_renders_empty_to_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Private threads")
    assert_contains(response, "You aren't participating in any private threads")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_to_user(default_category, user, user_client):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, "Test Thread")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_to_anonymous_user(default_category, client):
    post_thread(default_category, title="Test Thread")
    response = client.get(reverse("misago:threads"))
    assert_contains(response, "Test Thread")


def test_category_threads_list_displays_thread_to_user(
    default_category, user, user_client
):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, "Test Thread")


def test_category_threads_list_displays_thread_to_anonymous_user(
    default_category, client
):
    post_thread(default_category, title="Test Thread")
    response = client.get(default_category.get_absolute_url())
    assert_contains(response, "Test Thread")


def test_category_threads_list_displays_user_thread_to_user(
    default_category, user_client, other_user
):
    post_thread(default_category, title="Test Thread", poster=other_user)
    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, "Test Thread")


def test_category_threads_list_displays_user_thread_to_anonymous_user(
    default_category, client, other_user
):
    post_thread(default_category, title="Test Thread", poster=other_user)
    response = client.get(default_category.get_absolute_url())
    assert_contains(response, "Test Thread")


def test_category_threads_list_includes_child_category_thread(
    default_category, user, user_client, other_user
):
    default_category.list_children_threads = True
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    post_thread(child_category, title="Test Thread", poster=other_user)

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
    assert_contains(response, "Test Thread")


def test_category_threads_list_excludes_child_category_thread_if_list_children_threads_is_false(
    default_category, user, user_client, other_user
):
    default_category.list_children_threads = False
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    post_thread(child_category, title="Test Thread", poster=other_user)

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


def test_private_threads_list_displays_private_thread(
    private_threads_category, user, user_client
):
    thread = post_thread(private_threads_category, title="Test Private Thread")
    ThreadParticipant.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Test Private Thread")


def test_private_threads_list_displays_user_private_thread(
    private_threads_category, user, user_client, other_user
):
    thread = post_thread(
        private_threads_category, title="Test Private Thread", poster=other_user
    )
    ThreadParticipant.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Test Private Thread")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_empty_in_htmx_request(db, user_client):
    response = user_client.get(
        reverse("misago:threads"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_in_htmx_request(default_category, user_client):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(
        reverse("misago:threads"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")


def test_category_threads_list_displays_empty_in_htmx_request(
    default_category, user_client
):
    response = user_client.get(
        default_category.get_absolute_url(),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")


def test_category_threads_list_displays_thread_in_htmx_request(
    default_category, user_client
):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(
        default_category.get_absolute_url(),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")


def test_private__threads_list_displays_empty_in_htmx_request(db, user_client):
    response = user_client.get(
        reverse("misago:private-threads"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")


def test_private_threads_list_displays_thread_in_htmx_request(
    user, private_threads_category, user_client
):
    thread = post_thread(private_threads_category, title="Test Thread")
    ThreadParticipant.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-threads"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_with_animation_in_htmx_request(
    default_category, user_client
):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(
        reverse("misago:threads") + "?animate_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_contains(response, "threads-list-item-animate")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_without_animation_in_htmx_request(
    default_category, user_client
):
    thread = post_thread(default_category, title="Test Thread")
    response = user_client.get(
        reverse("misago:threads") + f"?animate_new={thread.last_post_id + 1}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_not_contains(response, "threads-list-item-animate")


@override_dynamic_settings(index_view="categories")
def test_threads_list_displays_thread_without_animation_without_htmx(
    default_category, user_client
):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(
        reverse("misago:threads") + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_not_contains(response, "threads-list-item-animate")


def test_category_threads_list_displays_thread_with_animation_in_htmx_request(
    default_category, user_client
):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(
        default_category.get_absolute_url() + "?animate_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_contains(response, "threads-list-item-animate")


def test_category_threads_list_displays_thread_without_animation_in_htmx_request(
    default_category, user_client
):
    thread = post_thread(default_category, title="Test Thread")
    response = user_client.get(
        default_category.get_absolute_url() + f"?animate_new={thread.last_post_id + 1}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_not_contains(response, "threads-list-item-animate")


def test_category_threads_list_displays_thread_without_animation_without_htmx(
    default_category, user_client
):
    post_thread(default_category, title="Test Thread")
    response = user_client.get(
        default_category.get_absolute_url() + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_not_contains(response, "threads-list-item-animate")


def test_private_threads_list_displays_thread_with_animation_in_htmx_request(
    private_threads_category, user_client, user
):
    thread = post_thread(private_threads_category, title="Test Thread")
    ThreadParticipant.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-threads") + "?animate_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_contains(response, "threads-list-item-animate")


def test_private_threads_list_displays_thread_without_animation_in_htmx_request(
    private_threads_category, user_client, user
):
    thread = post_thread(private_threads_category, title="Test Thread")
    ThreadParticipant.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-threads") + f"?animate_new={thread.last_post_id + 1}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_not_contains(response, "threads-list-item-animate")


def test_private_threads_list_displays_thread_without_animation_without_htmx(
    private_threads_category, user_client, user
):
    thread = post_thread(private_threads_category, title="Test Thread")
    ThreadParticipant.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-threads") + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, "Test Thread")
    assert_not_contains(response, "threads-list-item-animate")


@override_dynamic_settings(index_view="categories")
def test_threads_list_raises_404_error_if_filter_is_invalid(
    default_category, user, user_client
):
    post_thread(default_category, title="User Thread", poster=user)
    response = user_client.get(reverse("misago:threads", kwargs={"filter": "invalid"}))
    assert response.status_code == 404


@override_dynamic_settings(index_view="categories")
def test_threads_list_filters_threads(default_category, user, user_client):
    visible_thread = post_thread(default_category, title="User Thread", poster=user)
    hidden_thread = post_thread(default_category, title="Hidden Thread")

    response = user_client.get(reverse("misago:threads", kwargs={"filter": "my"}))
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@override_dynamic_settings(index_view="threads")
def test_index_threads_list_filters_threads(default_category, user, user_client):
    visible_thread = post_thread(default_category, title="User Thread", poster=user)
    hidden_thread = post_thread(default_category, title="Hidden Thread")

    response = user_client.get(reverse("misago:threads", kwargs={"filter": "my"}))
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@override_dynamic_settings(index_view="categories")
def test_threads_list_builds_valid_filters_urls(user_client):
    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, reverse("misago:threads", kwargs={"filter": "my"}))


@override_dynamic_settings(index_view="threads")
def test_index_threads_list_builds_valid_filters_urls(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, reverse("misago:threads", kwargs={"filter": "my"}))


def test_category_threads_list_raises_404_error_if_filter_is_invalid(
    default_category, user, user_client
):
    post_thread(default_category, title="User Thread", poster=user)
    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={
                "id": default_category.id,
                "slug": default_category.slug,
                "filter": "invalid",
            },
        )
    )
    assert response.status_code == 404


def test_category_threads_list_filters_threads(default_category, user, user_client):
    visible_thread = post_thread(default_category, title="User Thread", poster=user)
    hidden_thread = post_thread(default_category, title="Other Thread")

    response = user_client.get(
        reverse(
            "misago:category",
            kwargs={
                "id": default_category.id,
                "slug": default_category.slug,
                "filter": "my",
            },
        )
    )
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


def test_private_threads_list_raises_404_error_if_filter_is_invalid(
    private_threads_category, user, user_client
):
    thread = post_thread(private_threads_category, title="User Thread", poster=user)
    ThreadParticipant.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-threads", kwargs={"filter": "invalid"})
    )
    assert response.status_code == 404


def test_private_threads_list_filters_threads(
    private_threads_category, user, user_client
):
    visible_thread = post_thread(
        private_threads_category, title="User Thread", poster=user
    )
    hidden_thread = post_thread(private_threads_category, title="Other Thread")

    ThreadParticipant.objects.create(thread=visible_thread, user=user)
    ThreadParticipant.objects.create(thread=hidden_thread, user=user)

    response = user_client.get(
        reverse("misago:private-threads", kwargs={"filter": "my"})
    )
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@override_dynamic_settings(index_view="categories")
@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
def test_site_threads_list_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, db, client
):
    response = client.get(reverse("misago:threads"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:threads") + "?cursor=10"

    mock_pagination.assert_called_once()


@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
def test_category_threads_list_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, default_category, client
):
    response = client.get(default_category.get_absolute_url())

    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url() + "?cursor=10"

    mock_pagination.assert_called_once()


@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
def test_private_threads_list_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client
):
    response = user_client.get(reverse("misago:private-threads"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-threads") + "?cursor=10"

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
def test_site_threads_list_renders_unread_thread(user, user_client, default_category):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = post_thread(default_category, title="Unread Thread")

    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)


def test_category_threads_list_renders_unread_thread(
    user, user_client, default_category
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = post_thread(default_category, title="Unread Thread")

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)


def test_private_threads_list_renders_unread_thread(
    user, user_client, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = post_thread(private_threads_category, title="Unread Thread")

    ThreadParticipant.objects.create(thread=unread_thread, user=user)

    response = user_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)
