from django.urls import reverse

from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains, assert_not_contains


def test_thread_detail_view_shows_reply_button_to_anonymous_user_with_permission(
    client, thread
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_doesnt_show_reply_button_to_anonymous_user_without_permission(
    client, guests_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=guests_group, permission=CategoryPermission.REPLY
    ).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )
    assert_not_contains(response, "quick_reply")


def test_thread_detail_view_doesnt_show_quick_reply_to_anonymous_user_with_permission(
    client, thread
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(response, "quick_reply")


def test_thread_detail_view_doesnt_show_quick_reply_to_anonymous_user_without_permission(
    client, guests_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(response, "quick_reply")


def test_thread_detail_view_doesnt_show_reply_ui_to_anonymous_user_with_permission_in_closed_category(
    client, thread
):
    thread.category.is_closed = True
    thread.category.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_doesnt_show_reply_ui_to_anonymous_user_with_permission_in_closed_thread(
    client, thread
):
    thread.is_closed = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_shows_reply_button_to_user_with_permission(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_doesnt_show_reply_button_to_user_without_permission(
    user_client, members_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )
    assert_not_contains(response, "quick_reply")


def test_thread_detail_view_shows_quick_reply_to_user_with_permission(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(response, "quick_reply")


def test_thread_detail_view_doesnt_show_quick_reply_to_user_without_permission(
    user_client, members_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(response, "quick_reply")


def test_thread_detail_view_doesnt_show_reply_ui_to_user_with_permission_in_closed_category(
    user_client, thread
):
    thread.category.is_closed = True
    thread.category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_doesnt_show_reply_ui_to_user_with_permission_in_closed_thread(
    user_client, thread
):
    thread.is_closed = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_shows_reply_button_to_category_moderator_with_permission(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_doesnt_show_reply_button_to_category_moderator_without_permission(
    user_client, members_group, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )
    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_shows_quick_reply_to_category_moderator_with_permission(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(response, "quick_reply")


def test_thread_detail_view_doesnt_show_quick_reply_to_category_moderator_without_permission(
    user_client, members_group, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    CategoryGroupPermission.objects.filter(
        group=members_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(response, "quick_reply")


def test_thread_detail_view_shows_reply_ui_to_category_moderator_with_permission_in_closed_category(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.category.is_closed = True
    thread.category.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_shows_reply_ui_to_category_moderator_with_permission_in_closed_thread(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.is_closed = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_shows_reply_button_to_global_moderator_with_permission(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_doesnt_show_reply_button_to_global_moderator_without_permission(
    moderator_client, moderators_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=moderators_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_shows_quick_reply_to_global_moderator_with_permission(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(response, "quick_reply")


def test_thread_detail_view_doesnt_show_quick_reply_to_global_moderator_without_permission(
    moderator_client, moderators_group, thread
):
    CategoryGroupPermission.objects.filter(
        group=moderators_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_not_contains(response, "quick_reply")


def test_thread_detail_view_shows_reply_ui_to_global_moderator_with_permission_in_closed_category(
    moderator_client, thread
):
    thread.category.is_closed = True
    thread.category.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )


def test_thread_detail_view_shows_reply_ui_to_global_moderator_with_permission_in_closed_thread(
    moderator_client, thread
):
    thread.is_closed = True
    thread.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )

    assert_contains(response, thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread-reply", kwargs={"thread_id": thread.id, "slug": thread.slug}
        ),
    )
