import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...permissions.enums import CanUploadAttachments, CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import (
    assert_contains,
    assert_contains_element,
    assert_not_contains,
    assert_not_contains_element,
)


def test_thread_edit_view_displays_login_page_to_guests(client, user_thread):
    response = client.get(
        reverse(
            "misago:thread-edit",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to edit threads")


def test_thread_edit_view_displays_error_404_to_users_without_see_category_permission(
    user_client, user, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert response.status_code == 404


def test_thread_edit_view_displays_error_404_to_users_without_browse_category_permission(
    user_client, user, user_thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert response.status_code == 404


def test_thread_edit_view_displays_error_404_to_users_who_cant_see_thread(
    user_client, hidden_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={"thread_id": hidden_thread.id, "slug": hidden_thread.slug},
        )
    )
    assert response.status_code == 404


def test_thread_edit_view_displays_error_403_to_users_who_cant_edit_threads(
    user_client, members_group, user_thread
):
    members_group.can_edit_own_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={
                "thread_id": user_thread.id,
                "slug": user_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit threads.", 403)


def test_thread_edit_view_displays_error_403_to_users_who_cant_edit_other_users_threads(
    user_client, other_user_thread
):
    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={
                "thread_id": other_user_thread.id,
                "slug": other_user_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; threads.", 403)


def test_thread_edit_view_displays_error_403_to_users_who_cant_edit_deleted_users_threads(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t edit other users&#x27; threads.", 403)


def test_thread_edit_view_displays_error_403_to_users_without_closed_category_permission(
    user_client, default_category, user_thread
):
    default_category.is_closed = True
    default_category.save()

    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert_contains(response, "This category is closed.", 403)


def test_thread_edit_view_displays_error_403_to_users_without_closed_thread_permission(
    user_client, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    response = user_client.get(
        reverse(
            "misago:thread-edit",
            kwargs={"thread_id": user_thread.id, "slug": user_thread.slug},
        )
    )
    assert_contains(response, "This thread is closed.", 403)
