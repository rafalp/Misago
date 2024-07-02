from django.urls import reverse

from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..models import ThreadParticipant
from ..test import post_thread


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_empty_to_guests(db, client):
    response = client.get(reverse("misago:threads"))
    assert response.status_code == 200


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:threads"))
    assert response.status_code == 200


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_renders_empty_to_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:threads"))
    assert response.status_code == 200


def test_category_threads_list_renders_empty_to_guests(default_category, client):
    response = client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)


def test_category_threads_list_renders_empty_to_users(default_category, user_client):
    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)


def test_category_threads_list_renders_empty_to_moderators(
    default_category, moderator_client
):
    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, default_category.name)


def test_child_category_threads_list_renders_empty_to_guests(child_category, client):
    response = client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)


def test_child_category_threads_list_renders_empty_to_users(
    child_category, user_client
):
    response = user_client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)


def test_child_category_threads_list_renders_empty_to_moderators(
    child_category, moderator_client
):
    response = moderator_client.get(child_category.get_absolute_url())
    assert_contains(response, child_category.name)


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


def test_private_threads_list_shows_permission_error_to_users_without_permission(
    user_client, members_group
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(reverse("misago:private-threads"))
    print(response.content)
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_threads_list_renders_empty_to_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:private-threads"))
    assert_contains(response, "Private threads")


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
    assert_not_contains(response, "Test Thread")


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
