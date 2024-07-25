from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.models import Moderator
from ...test import assert_contains, assert_not_contains
from ..test import post_thread

MODERATION_FORM_HTML = '<form id="threads-moderation" method="post">'
MODERATION_FIXED_HTML = '<div class="fixed-moderation">'
DISABLED_CHECKBOX_HTML = '<input type="checkbox" disabled />'


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_shows_noscript_moderation_form_to_moderators(
    default_category, moderator_client
):
    response = moderator_client.get(reverse("misago:threads"))
    assert_contains(response, MODERATION_FORM_HTML)


def test_category_threads_list_shows_noscript_moderation_form_to_moderators(
    default_category, moderator_client
):
    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, MODERATION_FORM_HTML)


@override_dynamic_settings(index_view="categories")
def test_site_threads_list_shows_fixed_moderation_form_to_moderators(
    default_category, moderator_client
):
    response = moderator_client.get(reverse("misago:threads"))
    assert_contains(response, MODERATION_FIXED_HTML)


def test_category_threads_list_shows_fixed_moderation_form_to_moderators(
    default_category, moderator_client
):
    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, MODERATION_FIXED_HTML)


@override_dynamic_settings(index_view="categories")
def test_site_threads_doesnt_show_moderation_to_users(default_category, user_client):
    response = user_client.get(reverse("misago:threads"))
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


def test_category_threads_list_doesnt_show_moderation_to_users(
    default_category, user_client
):
    response = user_client.get(default_category.get_absolute_url())
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


@override_dynamic_settings(index_view="categories")
def test_site_threads_doesnt_show_moderation_to_guests(default_category, user_client):
    response = user_client.get(reverse("misago:threads"))
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


def test_category_threads_list_doesnt_show_moderation_to_guests(
    default_category, user_client
):
    response = user_client.get(default_category.get_absolute_url())
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


def test_category_threads_list_doesnt_show_moderation_to_other_category_moderators(
    default_category, child_category, user, user_client
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(child_category.get_absolute_url())
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


@override_dynamic_settings(index_view="categories")
def test_site_threads_shows_threads_checkboxes_to_global_moderators(
    default_category, moderator_client
):
    thread = post_thread(default_category, "Moderate Thread")

    response = moderator_client.get(reverse("misago:threads"))
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


def test_category_threads_shows_threads_checkboxes_to_global_moderators(
    default_category, moderator_client
):
    thread = post_thread(default_category, "Moderate Thread")

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


@override_dynamic_settings(index_view="categories")
def test_site_threads_shows_threads_checkboxes_to_category_moderators(
    default_category, user, user_client
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = post_thread(default_category, "Moderate Thread")

    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


def test_category_threads_shows_threads_checkboxes_to_category_moderators(
    default_category, user, user_client
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = post_thread(default_category, "Moderate Thread")

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


@override_dynamic_settings(index_view="categories")
def test_site_threads_shows_disabled_threads_checkboxes_to_other_category_moderators(
    default_category, child_category, user, user_client
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = post_thread(child_category, "Moderate Thread")

    response = user_client.get(reverse("misago:threads"))
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_contains(response, DISABLED_CHECKBOX_HTML)


def test_category_threads_shows_disabled_threads_checkboxes_to_other_category_moderators(
    default_category, child_category, user, user_client
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = post_thread(child_category, "Moderate Thread")

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_contains(response, DISABLED_CHECKBOX_HTML)
