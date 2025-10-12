from datetime import timedelta

from django.urls import reverse

from ...categories.enums import CategoryChildrenComponent
from ...categories.models import Category
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains


def test_category_thread_list_view_returns_error_404_if_category_doesnt_exist(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id * 100,
                "slug": default_category.slug,
            },
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_if_guest_cant_see_it(
    client, sibling_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_if_user_cant_see_it(
    user_client, sibling_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_404_if_global_moderator_cant_see_it(
    moderator_client, sibling_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert response.status_code == 404


def test_category_thread_list_view_returns_error_403_if_guest_cant_browse_it(
    client, guests_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )

    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_category_thread_list_view_returns_error_403_if_user_cant_browse_it(
    user_client, members_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_category_thread_list_view_returns_error_403_if_global_moderator_cant_browse_it(
    moderator_client, moderators_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )

    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(
        response,
        "You can&#x27;t browse the contents of this category.",
        status_code=403,
    )


def test_category_thread_list_view_renders_if_guest_cant_browse_it_but_check_is_delayed(
    client, guests_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )

    sibling_category.delay_browse_check = True
    sibling_category.save()

    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(response, sibling_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_if_user_cant_browse_it_but_check_is_delayed(
    user_client, members_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )

    sibling_category.delay_browse_check = True
    sibling_category.save()

    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(response, sibling_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_if_global_moderator_cant_browse_it_but_check_is_delayed(
    moderator_client, moderators_group, sibling_category
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=moderators_group,
        permission=CategoryPermission.SEE,
    )

    sibling_category.delay_browse_check = True
    sibling_category.save()

    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": sibling_category.id, "slug": sibling_category.slug},
        )
    )
    assert_contains(response, sibling_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_returns_redirect_to_valid_url_if_slug_is_invalid(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={
                "category_id": default_category.id,
                "slug": "invalid",
            },
        )
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:category-thread-list",
        kwargs={
            "category_id": default_category.id,
            "slug": default_category.slug,
        },
    )


def test_category_thread_list_view_renders_full_subcategories_component(
    client, guests_group, default_category
):
    default_category.children_categories_component = CategoryChildrenComponent.FULL
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
    assert_contains(response, "list-group-category")


def test_category_thread_list_view_renders_dropdown_subcategories_component(
    client, guests_group, default_category
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


def test_category_thread_list_view_renders_empty_to_guests(client, default_category):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_users(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_global_moderators(
    moderator_client, default_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        )
    )
    assert_contains(response, default_category.name)
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_guests_in_htmx(
    client, default_category
):
    response = client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_users_in_htmx(
    user_client, default_category
):
    response = user_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_renders_empty_to_global_moderators_in_htmx(
    moderator_client, default_category
):
    response = moderator_client.get(
        reverse(
            "misago:category-thread-list",
            kwargs={"category_id": default_category.id, "slug": default_category.slug},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No threads have been started in this category yet")


def test_category_thread_list_view_marks_unread_category_without_unread_threads_as_read(
    thread_factory, user_client, user, default_category
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    threads = (
        thread_factory(
            default_category,
            started_on=-900,
        ),
        thread_factory(
            default_category,
            started_on=-600,
        ),
    )

    for thread in threads:
        ReadThread.objects.create(
            user=user,
            category=default_category,
            thread=thread,
            read_time=thread.last_post_on,
        )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    ReadCategory.objects.get(user=user, category=default_category)


def test_category_thread_list_view_marks_unread_category_with_read_entry_without_unread_threads_as_read(
    thread_factory, user_client, user, default_category
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    thread = thread_factory(
        default_category,
        started_on=-2400,
    )

    read_category = ReadCategory.objects.create(
        user=user,
        category=default_category,
        read_time=thread.last_post_on,
    )

    read_thread = thread_factory(
        default_category,
        started_on=-1200,
    )

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=read_thread,
        read_time=read_thread.last_post_on,
    )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    new_read_category = ReadCategory.objects.get(user=user, category=default_category)
    assert new_read_category.id == read_category.id
    assert new_read_category.read_time > read_category.read_time


def test_category_thread_list_view_doesnt_mark_unread_category_with_unread_thread_as_read(
    thread_factory, user_client, user, default_category
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    read_thread = thread_factory(
        default_category,
        started_on=-900,
    )

    ReadThread.objects.create(
        user=user,
        category=default_category,
        thread=read_thread,
        read_time=read_thread.last_post_on,
    )

    thread_factory(
        default_category,
        started_on=-600,
    )

    default_category.synchronize()
    default_category.save()

    response = user_client.get(default_category.get_absolute_url())
    assert response.status_code == 200

    assert ReadThread.objects.exists()
    assert not ReadCategory.objects.exists()
