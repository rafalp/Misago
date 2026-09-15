from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ...users.models import Group


def get_form_data(group: Group) -> dict:
    return {
        "name": group.name,
        "slug": group.slug,
        "description": group.description or "",
        "meta_description": group.meta_description or "",
        "color": group.color or "",
        "icon": group.icon or "",
        "css_suffix": group.css_suffix or "",
        "user_title": group.user_title or "",
        "is_page": "1" if group.is_page else "",
        "is_hidden": "1" if group.is_hidden else "",
        "can_search": str(group.can_search),
        "can_edit_own_threads": str(group.can_edit_own_threads),
        "own_threads_edit_time_limit": str(group.own_threads_edit_time_limit),
        "can_edit_own_posts": str(group.can_edit_own_posts),
        "own_posts_edit_time_limit": str(group.own_posts_edit_time_limit),
        "can_see_others_post_edits": str(group.can_see_others_post_edits),
        "can_hide_own_post_edits": str(group.can_hide_own_post_edits),
        "own_post_edits_hide_time_limit": str(group.own_post_edits_hide_time_limit),
        "own_delete_post_edits_time_limit": str(group.own_delete_post_edits_time_limit),
        "bypass_flood_control": str(group.bypass_flood_control),
        "bypass_content_approval": str(group.bypass_content_approval),
        "can_use_private_threads": str(group.can_use_private_threads),
        "can_start_private_threads": str(group.can_start_private_threads),
        "private_thread_members_limit": str(group.private_thread_members_limit),
        "can_upload_attachments": str(group.can_upload_attachments),
        "attachment_storage_limit": str(group.attachment_storage_limit),
        "unused_attachments_storage_limit": str(group.unused_attachments_storage_limit),
        "attachment_size_limit": str(group.attachment_size_limit),
        "can_always_delete_own_attachments": str(
            group.can_always_delete_own_attachments
        ),
        "can_start_polls": str(group.can_start_polls),
        "can_edit_own_polls": str(group.can_edit_own_polls),
        "own_polls_edit_time_limit": str(group.own_polls_edit_time_limit),
        "can_close_own_polls": str(group.can_close_own_polls),
        "own_polls_close_time_limit": str(group.own_polls_close_time_limit),
        "can_vote_in_polls": str(group.can_vote_in_polls),
        "can_like_posts": str(group.can_like_posts),
        "can_see_own_post_likes": str(group.can_see_own_post_likes),
        "can_see_others_post_likes": str(group.can_see_others_post_likes),
        "can_select_own_thread_solutions": str(group.can_select_own_thread_solutions),
        "can_change_own_thread_solutions": str(group.can_change_own_thread_solutions),
        "own_thread_solutions_change_time_limit": str(
            group.own_thread_solutions_change_time_limit
        ),
        "can_clear_own_thread_solutions": str(group.can_clear_own_thread_solutions),
        "own_thread_solutions_clear_time_limit": str(
            group.own_thread_solutions_clear_time_limit
        ),
        "can_change_username": str(group.can_change_username),
        "username_changes_limit": str(group.username_changes_limit),
        "username_changes_expire": str(group.username_changes_expire),
        "username_changes_span": str(group.username_changes_span),
        "can_see_user_profiles": str(group.can_see_user_profiles),
    }


def test_edit_group_form_is_rendered(admin_client, custom_group):
    response = admin_client.get(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id})
    )
    assert response.status_code == 200


def test_edit_group_form_updates_name(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["name"] = "New Name"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.name == "New Name"


def test_edit_group_form_sets_custom_slug(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["slug"] = "customized"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.slug == "customized"


def test_edit_group_form_validates_slug(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["slug"] = "invalid!"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert_contains(
        response,
        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
    )

    custom_group.refresh_from_db()
    assert custom_group.slug == "custom-group"


def test_edit_group_form_sets_slug_from_name_if_its_empty(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["name"] = "New Name"
    form_data["slug"] = ""

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.slug == "new-name"


def test_edit_group_form_validates_color(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["color"] = "invalid"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert_contains(response, "Entered value is not a valid color")

    custom_group.refresh_from_db()
    assert custom_group.color is None


def test_edit_group_form_validates_css_suffix(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["css_suffix"] = "invalid!"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert_contains(response, "Enter a valid CSS class name")

    custom_group.refresh_from_db()
    assert custom_group.css_suffix is None


def test_edit_group_form_validates_unused_attachments_limit_is_smaller_than_total_limit(
    admin_client, custom_group
):
    form_data = get_form_data(custom_group)
    form_data["attachment_storage_limit"] = "10"
    form_data["unused_attachments_storage_limit"] = "20"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert_contains(
        response,
        "Unused attachments limit cannot exceed total attachments limit.",
    )

    custom_group.refresh_from_db()
    assert custom_group.attachment_storage_limit == 512
    assert custom_group.unused_attachments_storage_limit == 64


def test_edit_group_form_allows_unused_attachments_limit_smaller_than_total_limit(
    admin_client, custom_group
):
    form_data = get_form_data(custom_group)
    form_data["attachment_storage_limit"] = "20"
    form_data["unused_attachments_storage_limit"] = "10"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.attachment_storage_limit == 20
    assert custom_group.unused_attachments_storage_limit == 10


def test_edit_group_form_allows_unused_attachments_limit_smaller_than_disabled_total_limit(
    admin_client, custom_group
):
    form_data = get_form_data(custom_group)
    form_data["attachment_storage_limit"] = "0"
    form_data["unused_attachments_storage_limit"] = "10"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.attachment_storage_limit == 0
    assert custom_group.unused_attachments_storage_limit == 10


def test_edit_group_form_updates_appearance_settings(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["icon"] = "fas fa-shield"
    form_data["css_suffix"] = "lorem-ipsum"
    form_data["user_title"] = "Customer"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.icon == "fas fa-shield"
    assert custom_group.css_suffix == "lorem-ipsum"
    assert custom_group.user_title == "Customer"


def test_edit_group_form_copies_group_permissions(
    admin_client, custom_group, members_group, other_category
):
    form_data = get_form_data(custom_group)
    form_data["copy_permissions"] = str(members_group.id)

    CategoryGroupPermission.objects.create(
        group=members_group,
        category=other_category,
        permission="copied",
    )

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    CategoryGroupPermission.objects.get(
        group=custom_group,
        category=other_category,
        permission="copied",
    )


def test_edit_group_form_sets_group_description_and_meta_description(
    admin_client, custom_group
):
    form_data = get_form_data(custom_group)
    form_data["description"] = "Hello **world**!"
    form_data["meta_description"] = "Hello meta description!"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.description == "Hello **world**!"
    assert custom_group.description_parsed == "<p>Hello <strong>world</strong>!</p>"
    assert custom_group.meta_description == "Hello meta description!"


def test_edit_group_form_sets_group_description_and_automatic_meta_description(
    admin_client, custom_group
):
    form_data = get_form_data(custom_group)
    form_data["description"] = "Hello **world**!"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.description == "Hello **world**!"
    assert custom_group.description_parsed == "<p>Hello <strong>world</strong>!</p>"
    assert custom_group.meta_description == "Hello world!"


def test_edit_group_form_clears_group_description_and_meta_description(
    admin_client, custom_group
):
    custom_group.description = "Hello **world**!"
    custom_group.description_parsed = "<p>Hello <strong>world</strong>!</p>"
    custom_group.meta_description = "Hello meta description!"
    custom_group.save()

    form_data = get_form_data(custom_group)
    form_data["description"] = ""
    form_data["meta_description"] = ""

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.description is None
    assert custom_group.description_parsed is None
    assert custom_group.meta_description is None


def test_edit_group_form_invalidates_groups_cache(admin_client, custom_group):
    with assert_invalidates_cache(CacheName.GROUPS):
        admin_client.post(
            reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
            get_form_data(custom_group),
        )


def test_edit_group_form_invalidates_permissions_cache(admin_client, custom_group):
    with assert_invalidates_cache(CacheName.PERMISSIONS):
        admin_client.post(
            reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
            get_form_data(custom_group),
        )
