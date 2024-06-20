from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains
from ...users.models import Group


def get_form_data(group: Group) -> dict:
    return {
        "group-name": group.name,
        "group-slug": group.slug,
        "group-color": group.color or "",
        "group-icon": group.icon or "",
        "group-css_suffix": group.css_suffix or "",
        "group-user_title": group.user_title or "",
        "group-is_page": "1" if group.is_page else "",
        "group-is_hidden": "1" if group.is_hidden else "",
        "group-can_use_private_threads": "1" if group.can_use_private_threads else "",
        "group-can_change_username": "1" if group.can_change_username else "",
        "group-username_changes_limit": str(group.username_changes_limit),
        "group-username_changes_expire": str(group.username_changes_expire),
        "group-username_changes_span": str(group.username_changes_span),
        "group-can_see_user_profiles": "1" if group.can_see_user_profiles else "",
    }


def test_edit_group_form_is_rendered(admin_client, custom_group):
    response = admin_client.get(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id})
    )
    assert response.status_code == 200


def test_edit_group_form_updates_name(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["group-name"] = "New Name"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.name == "New Name"


def test_edit_group_form_sets_custom_slug(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["group-slug"] = "customized"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.slug == "customized"


def test_edit_group_form_validates_slug(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["group-slug"] = "invalid!"

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
    form_data["group-name"] = "New Name"
    form_data["group-slug"] = ""

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.refresh_from_db()
    assert custom_group.slug == "new-name"


def test_edit_group_form_validates_color(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["group-color"] = "invalid"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert_contains(response, "Entered value is not a valid color")

    custom_group.refresh_from_db()
    assert custom_group.css_suffix is None


def test_edit_group_form_validates_css_suffix(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["group-css_suffix"] = "invalid!"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert_contains(response, "Enter a valid CSS class name")

    custom_group.refresh_from_db()
    assert custom_group.css_suffix is None


def test_edit_group_form_updates_appearance_settings(admin_client, custom_group):
    form_data = get_form_data(custom_group)
    form_data["group-icon"] = "fas fa-shield"
    form_data["group-css_suffix"] = "lorem-ipsum"
    form_data["group-user_title"] = "Customer"

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
    form_data["group-copy_permissions"] = str(members_group.id)

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
    form_data["description-markdown"] = "Hello **world**!"
    form_data["description-meta"] = "Hello meta description!"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.description.refresh_from_db()
    assert custom_group.description.markdown == "Hello **world**!"
    assert custom_group.description.html == "<p>Hello <strong>world</strong>!</p>"
    assert custom_group.description.meta == "Hello meta description!"


def test_edit_group_form_sets_group_description_and_automatic_meta_description(
    admin_client, custom_group
):
    form_data = get_form_data(custom_group)
    form_data["description-markdown"] = "Hello **world**!"

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.description.refresh_from_db()
    assert custom_group.description.markdown == "Hello **world**!"
    assert custom_group.description.html == "<p>Hello <strong>world</strong>!</p>"
    assert custom_group.description.meta == "Hello world!"


def test_edit_group_form_clears_group_description_and_meta_description(
    admin_client, custom_group
):
    custom_group.description.markdown = "Hello **world**!"
    custom_group.description.html = "<p>Hello <strong>world</strong>!</p>"
    custom_group.description.meta = "Hello meta description!"
    custom_group.description.save()

    form_data = get_form_data(custom_group)
    form_data["description-markdown"] = ""
    form_data["description-meta"] = ""

    response = admin_client.post(
        reverse("misago:admin:groups:edit", kwargs={"pk": custom_group.id}),
        form_data,
    )
    assert response.status_code == 302

    custom_group.description.refresh_from_db()
    assert custom_group.description.markdown is None
    assert custom_group.description.html is None
    assert custom_group.description.meta is None


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
