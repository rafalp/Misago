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
        "icon": group.icon or "",
        "css_suffix": group.css_suffix or "",
        "user_title": group.user_title or "",
        "is_page": "1" if group.is_page else "",
        "is_hidden": "1" if group.is_hidden else "",
        "can_see_user_profiles": "1" if group.can_see_user_profiles else "",
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
