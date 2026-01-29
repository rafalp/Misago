from unittest.mock import patch

from django.urls import reverse

from ...categories.enums import CategoryChildrenComponent
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...pagination.cursor import EmptyPageError
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
def test_thread_list_view_renders_empty_to_anonymous_users(db, client):
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
def test_thread_list_view_renders_empty_to_anonymous_users_in_htmx(db, client):
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
def test_thread_list_view_on_site_index_renders_empty_to_anonymous_users(db, client):
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
def test_thread_list_view_on_site_index_renders_empty_to_anonymous_users_in_htmx(
    db, client
):
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


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_deleted_user_thread_to_anonymous_user(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_deleted_user_thread_to_user(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_deleted_user_thread_to_category_moderator(
    thread_factory, user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_deleted_user_thread_to_global_moderator(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_thread_to_anonymous_user(
    thread_factory, client, user, default_category
):
    thread = thread_factory(default_category, starter=user)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_thread_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_thread_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_thread_to_global_moderator(
    thread_factory, moderator_client, user, default_category
):
    thread = thread_factory(default_category, starter=user)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_own_thread_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_user_unapproved_thread_to_anonymous_user(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_unapproved=True)

    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_user_unapproved_thread_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_unapproved=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_unapproved_thread_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, starter=other_user, is_unapproved=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_unapproved_thread_to_global_moderator(
    thread_factory, moderator_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_unapproved=True)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_own_unapproved_thread_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_unapproved=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_user_hidden_thread_to_anonymous_user(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_hidden=True)

    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-hidden")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_user_hidden_thread_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_hidden=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-hidden")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_hidden_thread_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, starter=other_user, is_hidden=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-hidden")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_hidden_thread_to_global_moderator(
    thread_factory, moderator_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_hidden=True)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-hidden")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_user_own_hidden_thread_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, is_hidden=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-hidden")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_without_flags(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_globally_pinned_thread(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=2)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-globally")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_thread_pinned_in_category_flag_to_anonymous_user(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=1)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned-locally-elsewhere")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_thread_pinned_in_category_flag_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=1)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-pinned-locally-elsewhere")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_pinned_in_category_flag_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(default_category, starter=other_user, weight=1)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_pinned_in_category_flag_to_global_moderator(
    thread_factory, moderator_client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, weight=1)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-pinned-locally-elsewhere")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_with_poll(
    thread_factory, poll_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)
    poll_factory(thread)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-poll")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_solved_thread(
    thread_factory, thread_reply_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)
    thread.best_answer = thread_reply_factory(thread)
    thread.save()

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-answered")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_closed_thread(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user, is_closed=True)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-closed")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_thread_unapproved_posts_flag_to_anonymous_user(
    thread_factory, client, other_user, default_category
):
    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_thread_unapproved_posts_flag_to_user(
    thread_factory, user_client, other_user, default_category
):
    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_unapproved_posts_flag_to_category_moderator(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_unapproved_posts_flag_to_global_moderator(
    thread_factory, moderator_client, other_user, default_category
):
    thread = thread_factory(
        default_category, starter=other_user, has_unapproved_posts=True
    )

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_own_thread_unapproved_posts_flag_to_user(
    thread_factory, user_client, user, default_category
):
    thread = thread_factory(default_category, starter=user, has_unapproved_posts=True)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_not_contains(response, "thread-flags")
    assert_not_contains(response, "thread-flag-unapproved")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_deleted_user_thread_to_anonymous_user_if_category_show_started_only_is_enabled(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_deleted_user_thread_to_user_if_category_show_started_only_is_enabled(
    thread_factory, user_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_deleted_user_thread_to_category_moderator_if_category_show_started_only_is_enabled(
    thread_factory, user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_deleted_user_thread_to_global_moderator_if_category_show_started_only_is_enabled(
    thread_factory, moderator_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_user_thread_to_anonymous_user_if_category_show_started_only_is_enabled(
    thread_factory, client, other_user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_user_thread_to_user_if_category_show_started_only_is_enabled(
    thread_factory, user_client, other_user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_thread_to_category_moderator_if_category_show_started_only_is_enabled(
    thread_factory, user_client, user, other_user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_thread_to_global_moderator_if_category_show_started_only_is_enabled(
    thread_factory, moderator_client, other_user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=other_user)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_user_own_thread_to_user_if_category_show_started_only_is_enabled(
    thread_factory, user_client, user, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_globally_pinned_thread_to_anonymous_user_if_category_show_started_only_is_enabled(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=2)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_globally_pinned_thread_to_user_if_category_show_started_only_is_enabled(
    thread_factory, user_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=2)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_category_pinned_thread_to_anonymous_user_if_category_show_started_only_is_enabled(
    thread_factory, client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=1)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_category_pinned_thread_to_user_if_category_show_started_only_is_enabled(
    thread_factory, user_client, default_category
):
    default_category.show_started_only = True
    default_category.save()

    thread = thread_factory(default_category, weight=1)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_with_user_starter_and_deleted_last_poster(
    thread_factory, thread_reply_factory, client, user, default_category
):
    thread = thread_factory(default_category, starter=user)
    thread_reply_factory(thread)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_with_deleted_starter_and_user_last_poster(
    thread_factory, thread_reply_factory, client, user, default_category
):
    thread = thread_factory(default_category)
    thread_reply_factory(thread, poster=user)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_with_different_deleted_starter_and_last_poster(
    thread_factory, thread_reply_factory, client, default_category
):
    thread = thread_factory(default_category, starter="SomeStarter")
    thread_reply_factory(thread, poster="OtherPoster")

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_with_different_starter_and_last_poster(
    thread_factory, thread_reply_factory, client, user, other_user, default_category
):
    thread = thread_factory(default_category, starter=other_user)
    thread_reply_factory(thread, poster=user)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


@override_dynamic_settings(
    index_view="categories",
    threads_list_item_categories_component="breadcrumbs",
)
def test_thread_list_view_displays_category_thread_using_breadcrumbs_component(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(
    index_view="categories",
    threads_list_item_categories_component="labels",
)
def test_thread_list_view_displays_category_thread_using_labels_component(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(
    index_view="categories",
    threads_list_item_categories_component="breadcrumbs",
)
def test_thread_list_view_displays_child_category_thread_using_breadcrumbs_component(
    thread_factory, client, child_category
):
    thread = thread_factory(child_category)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(
    index_view="categories",
    threads_list_item_categories_component="labels",
)
def test_thread_list_view_displays_child_category_thread_using_labels_component(
    thread_factory, client, child_category
):
    thread = thread_factory(child_category)

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_includes_child_category_thread(
    thread_factory, client, guests_group, other_user, default_category
):
    default_category.list_children_threads = False
    default_category.save()

    child_category = Category(name="Child Category", slug="child-category")
    child_category.insert_at(default_category, position="last-child", save=True)

    thread = thread_factory(child_category, starter=other_user)

    CategoryGroupPermission.objects.create(
        category=child_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=child_category,
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    )

    response = client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_display_private_threads(
    user_client, user_private_thread
):
    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, user_private_thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_in_htmx(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(
        reverse("misago:thread-list"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_displays_thread_with_animation_in_htmx(
    thread_factory, user_client, default_category
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
def test_thread_list_view_displays_thread_without_animation_in_htmx(
    thread_factory, user_client, default_category
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
def test_thread_list_view_disables_animations_without_htmx(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.get(
        reverse("misago:thread-list") + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_raises_404_error_if_filter_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:thread-list", kwargs={"filter": "invalid"})
    )
    assert response.status_code == 404


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_filters_threads(
    thread_factory, user_client, user, default_category
):
    visible_thread = thread_factory(default_category, starter=user)
    hidden_thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list", kwargs={"filter": "my"}))
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_raises_404_error_if_filter_is_invalid(
    user_client,
):
    response = user_client.get(
        reverse("misago:thread-list", kwargs={"filter": "invalid"})
    )
    assert response.status_code == 404


@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_filters_threads(
    thread_factory, user_client, user, default_category
):
    visible_thread = thread_factory(default_category, starter=user)
    hidden_thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list", kwargs={"filter": "my"}))
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
@override_dynamic_settings(index_view="categories")
def test_thread_list_view_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client
):
    response = user_client.get(reverse("misago:thread-list"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list") + "?cursor=10"

    mock_pagination.assert_called_once()


@patch("misago.threads.views.list.paginate_queryset", side_effect=EmptyPageError(10))
@override_dynamic_settings(index_view="threads")
def test_thread_list_view_on_site_index_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client
):
    response = user_client.get(reverse("misago:index"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:index") + "?cursor=10"

    mock_pagination.assert_called_once()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_renders_unread_thread(
    thread_factory, user, user_client, default_category
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)
