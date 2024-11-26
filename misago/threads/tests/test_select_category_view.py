import pytest
from django.urls import reverse

from ...categories.models import Category
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ...testutils import grant_category_group_permissions


@pytest.fixture
def sibling_category(root_category, guests_group, members_group):
    category = Category(name="Sibling Category", slug="sibling-category")
    category.insert_at(root_category, position="last-child", save=True)

    grant_category_group_permissions(
        category,
        guests_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )
    grant_category_group_permissions(
        category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    return category


@pytest.fixture
def child_category(default_category, guests_group, members_group):
    category = Category(name="Sibling Category", slug="sibling-category")
    category.insert_at(default_category, position="last-child", save=True)

    grant_category_group_permissions(
        category,
        guests_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )
    grant_category_group_permissions(
        category,
        members_group,
        CategoryPermission.SEE,
        CategoryPermission.BROWSE,
        CategoryPermission.START,
    )

    return category


def test_select_category_view_displays_error_page_if_guest_cant_start_thread_in_any_category(
    client, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = client.get(reverse("misago:start-thread"))
    assert_contains(response, "You can&#x27;t start new threads.", status_code=403)


def test_select_category_view_displays_error_page_if_user_cant_start_thread_in_any_category(
    user_client, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "You can&#x27;t start new threads.", status_code=403)


def test_select_category_view_displays_error_message_in_htmx_if_guest_cant_start_thread_in_any_category(
    client, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(response, "You can't start new threads.")


def test_select_category_view_displays_error_message_in_htmx_if_user_cant_start_thread_in_any_category(
    user_client, default_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(response, "You can't start new threads.")


def test_select_category_view_displays_category_if_guest_can_start_thread_in_it(
    client, default_category
):
    response = client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_displays_category_if_user_can_start_thread_in_it(
    user_client, default_category
):
    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_displays_category_in_htmx_if_guest_can_start_thread_in_it(
    client, guests_group, default_category
):
    response = client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_displays_category_in_htmx_if_user_can_start_thread_in_it(
    user_client, default_category
):
    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_category_if_guest_cant_start_thread_in_it(
    client, default_category, sibling_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_category_in_htmx_if_guest_cant_start_thread_in_it(
    client, default_category, sibling_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_category_if_user_cant_start_thread_in_it(
    user_client, default_category, sibling_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_category_in_htmx_if_user_cant_start_thread_in_it(
    user_client, default_category, sibling_category
):
    CategoryGroupPermission.objects.filter(
        category=default_category, permission=CategoryPermission.START
    ).delete()

    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_empty_vanilla_category(
    user_client, default_category, sibling_category
):
    default_category.is_vanilla = True
    default_category.save()

    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_empty_vanilla_category_in_htmx(
    user_client, default_category, sibling_category
):
    default_category.is_vanilla = True
    default_category.save()

    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_includes_vanilla_category_with_children(
    user_client, default_category, child_category
):
    default_category.is_vanilla = True
    default_category.save()

    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": child_category.id, "slug": child_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_includes_vanilla_category_with_children_in_htmx(
    user_client, default_category, child_category
):
    default_category.is_vanilla = True
    default_category.save()

    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": child_category.id, "slug": child_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_child_category_if_user_cant_start_thread_in_it(
    user_client, default_category, child_category
):
    CategoryGroupPermission.objects.filter(
        category=child_category, permission=CategoryPermission.START
    ).delete()

    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": child_category.id, "slug": child_category.slug},
        ),
    )


def test_select_category_view_excludes_child_category_in_htmx_if_user_cant_start_thread_in_it(
    user_client, default_category, child_category
):
    CategoryGroupPermission.objects.filter(
        category=child_category, permission=CategoryPermission.START
    ).delete()

    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": child_category.id, "slug": child_category.slug},
        ),
    )


def test_select_category_view_includes_closed_category_if_user_can_post_in_it(
    user, user_client, default_category, members_group, moderators_group
):
    default_category.is_closed = True
    default_category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_includes_closed_category_in_htmx_if_user_can_post_in_it(
    user, user_client, default_category, members_group, moderators_group
):
    default_category.is_closed = True
    default_category.save()

    user.set_groups(members_group, [moderators_group])
    user.save()

    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )


def test_select_category_view_excludes_closed_category_if_user_cant_post_in_it(
    user_client, default_category, sibling_category
):
    sibling_category.is_closed = True
    sibling_category.save()

    response = user_client.get(reverse("misago:start-thread"))
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )


def test_select_category_view_excludes_closed_category_in_htmx_if_user_cant_post_in_it(
    user_client, default_category, sibling_category
):
    sibling_category.is_closed = True
    sibling_category.save()

    response = user_client.get(
        reverse("misago:start-thread"),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Start new thread in")
    assert_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": default_category.id, "slug": default_category.slug},
        ),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:start-thread",
            kwargs={"id": sibling_category.id, "slug": sibling_category.slug},
        ),
    )
