from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse

from ...pagination.cursor import EmptyPageError
from ...permissions.models import Moderator
from ...readtracker.models import ReadCategory, ReadThread
from ...test import assert_contains, assert_not_contains
from ...threads.models import Thread
from ..models import PrivateThreadMember


def test_private_thread_list_view_displays_login_required_page_to_anonymous_user(
    db, client
):
    response = client.get(reverse("misago:private-thread-list"))
    assert_contains(response, "Sign in to view private threads", status_code=401)


def test_private_thread_list_view_shows_error_403_to_users_without_private_threads_permission(
    user_client, members_group
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_thread_list_view_displays_start_thread_button_to_user_with_permission(
    user_client,
):
    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, reverse("misago:private-thread-start"))


def test_private_thread_list_view_hides_start_thread_button_from_user_without_permission(
    user, user_client
):
    user.group.can_start_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_not_contains(response, reverse("misago:private-thread-start"))


def test_private_thread_list_view_renders_empty_to_users(user_client):
    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, "Private threads")
    assert_contains(response, "You aren't participating in any private threads")


def test_private_thread_list_view_renders_empty_to_private_threads_moderators(
    user_client, user
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, "Private threads")
    assert_contains(response, "You aren't participating in any private threads")


def test_private_thread_list_view_renders_empty_to_global_moderators(moderator_client):
    response = moderator_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, "Private threads")
    assert_contains(response, "You aren't participating in any private threads")


def test_private_thread_list_view_renders_empty_in_htmx_request(user_client):
    response = user_client.get(
        reverse("misago:private-thread-list"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")


def test_private_thread_list_view_displays_deleted_user_thread_to_user(
    thread_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_deleted_user_thread_to_private_threads_moderator(
    thread_factory, user_client, user, private_threads_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_deleted_user_thread_to_global_moderator(
    thread_factory, moderator_client, moderator, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=moderator)

    response = moderator_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_user_thread_to_user(
    thread_factory, user_client, user, other_user, private_threads_category
):
    thread = thread_factory(private_threads_category, starter=other_user)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_user_thread_to_private_threads_moderator(
    thread_factory, user_client, user, other_user, private_threads_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread = thread_factory(private_threads_category, starter=other_user)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_user_private_thread_to_global_moderator(
    thread_factory, moderator_client, moderator, user, private_threads_category
):
    thread = thread_factory(private_threads_category, starter=user)
    PrivateThreadMember.objects.create(thread=thread, user=moderator)

    response = moderator_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_user_own_thread_to_user(
    thread_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category, starter=user)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_thread_with_user_starter_and_deleted_last_poster(
    thread_factory,
    thread_reply_factory,
    user_client,
    user,
    other_user,
    private_threads_category,
):
    thread = thread_factory(private_threads_category, starter=other_user)
    thread_reply_factory(thread)

    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


def test_private_thread_list_view_displays_thread_with_deleted_starter_and_user_last_poster(
    thread_factory, thread_reply_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category)
    thread_reply_factory(thread, poster=user)

    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


def test_private_thread_list_view_displays_thread_with_different_deleted_starter_and_last_poster(
    thread_factory, thread_reply_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category, starter="SomeStarter")
    thread_reply_factory(thread, poster="OtherPoster")

    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


def test_private_thread_list_view_displays_thread_with_different_starter_and_last_poster(
    thread_factory,
    thread_reply_factory,
    user_client,
    user,
    moderator,
    other_user,
    private_threads_category,
):
    thread = thread_factory(private_threads_category, starter=other_user)
    thread_reply_factory(thread, poster=moderator)

    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, thread.starter_name)
    assert_contains(response, thread.last_poster_name)


def test_private_thread_list_view_doesnt_display_threads(user_client, user_thread):
    response = user_client.get(reverse("misago:private-thread-list"))
    assert_not_contains(response, user_thread.title)


def test_private_thread_list_view_displays_thread_in_htmx(
    thread_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-thread-list"),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)


def test_private_thread_list_view_displays_thread_with_animation_in_htmx(
    thread_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-thread-list") + "?animate_new=0",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-animate")


def test_private_thread_list_view_displays_thread_without_animation_in_htmx(
    thread_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-thread-list")
        + f"?animate_new={thread.last_post_id + 1}",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


def test_private_thread_list_view_disables_animations_without_htmx(
    thread_factory, user_client, user, private_threads_category
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    response = user_client.get(
        reverse("misago:private-thread-list") + "?animate_new=0",
    )
    assert_contains(response, "<h1>")
    assert_contains(response, thread.title)
    assert_not_contains(response, "threads-list-item-animate")


def test_private_thread_list_view_raises_404_error_if_filter_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:private-thread-list", kwargs={"filter": "invalid"})
    )
    assert response.status_code == 404


def test_private_thread_list_view_filters_threads(
    thread_factory, user_client, user, private_threads_category
):
    visible_thread = thread_factory(private_threads_category, starter=user)
    hidden_thread = thread_factory(private_threads_category)

    PrivateThreadMember.objects.create(thread=visible_thread, user=user)
    PrivateThreadMember.objects.create(thread=hidden_thread, user=user)

    response = user_client.get(
        reverse("misago:private-thread-list", kwargs={"filter": "my"})
    )
    assert_contains(response, visible_thread.title)
    assert_not_contains(response, hidden_thread.title)


@patch(
    "misago.privatethreads.views.list.paginate_queryset", side_effect=EmptyPageError(10)
)
def test_private_thread_list_view_redirects_to_last_page_for_invalid_cursor(
    mock_pagination, user_client
):
    response = user_client.get(reverse("misago:private-thread-list"))

    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list") + "?cursor=10"

    mock_pagination.assert_called_once()


def test_private_thread_list_view_renders_unread_thread(
    thread_factory, user, user_client, private_threads_category
):
    user.joined_on = user.joined_on.replace(year=2012)
    user.save()

    unread_thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=unread_thread, user=user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert_contains(response, "Has unread posts")
    assert_contains(response, unread_thread.title)


def create_user_private_thread_memberships(user):
    for thread in Thread.objects.all():
        PrivateThreadMember.objects.create(user=user, thread=thread)


def test_private_thread_list_view_without_unread_threads_marks_category_as_read(
    thread_factory, private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    threads = (
        thread_factory(
            private_threads_category,
            started_at=-900,
        ),
        thread_factory(
            private_threads_category,
            started_at=-600,
        ),
    )

    for thread in threads:
        ReadThread.objects.create(
            user=user,
            category=private_threads_category,
            thread=thread,
            read_time=thread.last_posted_at,
        )

    private_threads_category.synchronize()
    private_threads_category.save()

    create_user_private_thread_memberships(user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    ReadCategory.objects.get(user=user, category=private_threads_category)


def test_private_thread_list_view_without_unread_threads_clears_user_unread_threads_count(
    thread_factory, private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.unread_private_threads = 50
    user.save()

    threads = (
        thread_factory(
            private_threads_category,
            started_at=-900,
        ),
        thread_factory(
            private_threads_category,
            started_at=-600,
        ),
    )

    for thread in threads:
        ReadThread.objects.create(
            user=user,
            category=private_threads_category,
            thread=thread,
            read_time=thread.last_posted_at,
        )

    private_threads_category.synchronize()
    private_threads_category.save()

    create_user_private_thread_memberships(user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.unread_private_threads == 0


def test_private_thread_list_view_with_read_entry_without_unread_threads_marks_category_as_read(
    thread_factory, private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    thread = thread_factory(
        private_threads_category,
        started_at=-2400,
    )

    read_category = ReadCategory.objects.create(
        user=user,
        category=private_threads_category,
        read_time=thread.last_posted_at,
    )

    read_thread = thread_factory(
        private_threads_category,
        started_at=-1200,
    )

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=read_thread,
        read_time=read_thread.last_posted_at,
    )

    private_threads_category.synchronize()
    private_threads_category.save()

    create_user_private_thread_memberships(user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert response.status_code == 200

    assert not ReadThread.objects.exists()

    new_read_category = ReadCategory.objects.get(
        user=user, category=private_threads_category
    )
    assert new_read_category.id == read_category.id
    assert new_read_category.read_time > read_category.read_time


def test_private_thread_list_view_with_unread_thread_doesnt_mark_category_as_read(
    thread_factory, private_threads_category, user, user_client
):
    user.joined_on -= timedelta(minutes=60)
    user.save()

    read_thread = thread_factory(
        private_threads_category,
        started_at=-900,
    )

    ReadThread.objects.create(
        user=user,
        category=private_threads_category,
        thread=read_thread,
        read_time=read_thread.last_posted_at,
    )

    thread_factory(
        private_threads_category,
        started_at=-600,
    )

    private_threads_category.synchronize()
    private_threads_category.save()

    create_user_private_thread_memberships(user)

    response = user_client.get(reverse("misago:private-thread-list"))
    assert response.status_code == 200

    assert ReadThread.objects.exists()
    assert not ReadCategory.objects.exists()
