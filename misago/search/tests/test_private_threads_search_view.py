from datetime import date, timedelta

from django.test import override_settings
from django.urls import reverse

from ...privatethreads.models import PrivateThreadMember
from ...test import assert_contains, assert_not_contains
from ..enums import SearchMode, SearchSort
from ..models import SearchLog
from ..threads import threads_search


def test_private_threads_search_view_returns_sign_in_page_if_user_is_not_signed_in(
    db, client
):
    response = client.get(reverse("misago:private-threads-search"))
    assert_contains(response, "Sign in to search private threads", status_code=401)


def test_private_threads_search_view_returns_error_403_if_user_is_not_signed_in_in_htmx(
    db, client
):
    response = client.get(
        reverse("misago:private-threads-search"), headers={"hx-request": "true"}
    )
    assert_contains(response, "Sign in to search private threads", status_code=403)


def test_private_threads_search_view_returns_error_403_if_user_cant_search(
    user_client, user
):
    user.group.can_search = False
    user.group.save()

    response = user_client.get(reverse("misago:private-threads-search"))
    assert_contains(response, "You can&#x27;t search this site.", status_code=403)


def test_private_threads_search_view_returns_error_403_if_user_cant_use_private_threads(
    user_client, user
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(reverse("misago:private-threads-search"))
    assert_contains(response, "You can&#x27;t use private threads.", status_code=403)


def test_private_threads_search_view_shows_user_threads_result(
    user_client, user_private_thread
):
    threads_search.index_thread(user_private_thread)
    threads_search.index_post(
        user_private_thread.first_post, user_private_thread.first_post.content
    )

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=Thread"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_user_posts_result(
    user_client, user_private_thread
):
    threads_search.index_thread(user_private_thread)
    threads_search.index_post(user_private_thread.first_post, "Content")

    response = user_client.get(
        reverse("misago:private-threads-search")
        + f"?query=Content&mode={SearchMode.POSTS}"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_user_thread_titles_result(
    user_client, user_private_thread
):
    threads_search.index_thread(user_private_thread)
    threads_search.index_post(
        user_private_thread.first_post, user_private_thread.first_post.content
    )

    response = user_client.get(
        reverse("misago:private-threads-search")
        + f"?query=Thread&mode={SearchMode.THREAD_TITLES}"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_deleted_user_threads_result(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    threads_search.index_thread(private_thread)
    threads_search.index_post(
        private_thread.first_post, private_thread.first_post.content
    )

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=Thread"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_deleted_user_posts_result(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    threads_search.index_thread(private_thread)
    threads_search.index_post(private_thread.first_post, "Content")

    response = user_client.get(
        reverse("misago:private-threads-search")
        + f"?query=Content&mode={SearchMode.POSTS}"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_deleted_user_thread_titles_result(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    threads_search.index_thread(private_thread)
    threads_search.index_post(
        private_thread.first_post, private_thread.first_post.content
    )

    response = user_client.get(
        reverse("misago:private-threads-search")
        + f"?query=Thread&mode={SearchMode.THREAD_TITLES}"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_results_in_htmx(
    user_client, user_private_thread
):
    threads_search.index_thread(user_private_thread)
    threads_search.index_post(
        user_private_thread.first_post, user_private_thread.first_post.content
    )

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=Thread",
        headers={"hx-request": "true"},
    )

    assert_not_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_no_results_page(user_client):
    response = user_client.get(reverse("misago:private-threads-search") + "?query=test")

    assert_contains(response, "Search private threads")
    assert_contains(response, "No private threads found")


def test_private_threads_search_view_shows_no_results_page_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test",
        headers={"hx-request": "true"},
    )

    assert_not_contains(response, "Search private threads")
    assert_contains(response, "No private threads found")


def test_private_threads_search_view_shows_no_results_page_for_offset(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=10"
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, "No private threads found")


def test_private_threads_search_view_shows_no_results_page_for_offset_in_htmx(
    user_client,
):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=10",
        headers={"hx-request": "true"},
    )

    assert_not_contains(response, "Search private threads")
    assert_contains(response, "No private threads found")


def test_private_threads_search_view_returns_404_for_invalid_offset(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=invalid"
    )
    assert response.status_code == 404


def test_private_threads_search_view_returns_404_for_invalid_offset_in_htmx(
    user_client,
):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=invalid",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_private_threads_search_view_returns_404_for_negative_offset(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=-1"
    )
    assert response.status_code == 404


def test_private_threads_search_view_returns_404_for_negative_offset_in_htmx(
    user_client,
):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=-1",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_private_threads_search_view_returns_404_for_max_offset(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=1000"
    )
    assert response.status_code == 404


def test_private_threads_search_view_returns_404_for_max_offset_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=test&offset=1000",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


@override_settings(MISAGO_THREADS_SEARCH={"RESULT_SIZE": 1})
def test_private_threads_search_view_shows_results_with_next_page(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem ipsum"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
        ),
    )
    assert_contains(response, "Load more")
    assert_contains(
        response,
        reverse("misago:private-threads-search")
        + "?query=lorem+ipsum&amp;mode=threads&amp;sort=relevance&amp;offset=1",
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_results_without_next_page(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem ipsum"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_contains(
        response,
        reverse(
            "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
        ),
    )
    assert_not_contains(response, "Load more")
    assert_not_contains(response, "offset=")
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_results_after_offset(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem ipsum&offset=1"
    )

    assert_contains(response, "Search private threads")
    assert_not_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_contains(
        response,
        reverse(
            "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
        ),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_error_if_query_is_empty(user_client):
    response = user_client.get(reverse("misago:private-threads-search"))

    assert_contains(response, "Search private threads")
    assert_contains(response, "This field is required.")
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_error_if_query_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=-lorem"
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, "This search query is too broad.")
    assert_not_contains(response, "No private threads found")


@override_settings(MISAGO_THREADS_SEARCH={"RESULT_SIZE": 1})
def test_private_threads_search_view_keeps_search_query_in_more_url(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem"
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, reverse("misago:private-threads-search") + "?query=lorem")


def test_private_threads_search_view_shows_error_if_users_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem&users=invalid"
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, "One or more users not found: invalid")
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_uses_users_search_option(
    user_client, user, user_private_thread, other_user_private_thread
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + f"?query=lorem&users={user.slug}"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(
        response,
        reverse(
            "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
        ),
    )
    assert_not_contains(response, "No private threads found")


@override_settings(MISAGO_THREADS_SEARCH={"RESULT_SIZE": 1})
def test_private_threads_search_view_keeps_users_in_more_url(
    user_client, user, other_user, user_private_thread, other_user_private_thread
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search")
        + f"?query=lorem&users={user.slug},{other_user.slug}"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:private-threads-search")
        + "?query=lorem&amp;mode=threads&amp;sort=relevance"
        + f"&amp;users={user.slug}%2C+{other_user.slug}",
    )


def test_private_threads_search_view_shows_error_if_mode_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem&mode=invalid"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response, "Select a valid choice. invalid is not one of the available choices"
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_shows_error_if_sort_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem&mode=invalid"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response, "Select a valid choice. invalid is not one of the available choices"
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_uses_sort_search_option(
    user_client, user_private_thread, other_user_private_thread
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem latin ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search")
        + f"?query=lorem+ipsum&sort={SearchSort.NEWEST}"
    )

    user_thread_url = reverse(
        "misago:post", kwargs={"post_id": user_private_thread.first_post.id}
    )
    other_user_thread_url = reverse(
        "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, user_thread_url)
    assert_contains(response, other_user_thread_url)
    assert_not_contains(response, "No private threads found")

    response_content = response.content.decode()
    user_thread_index = response_content.index(user_thread_url)
    other_user_thread_index = response_content.index(other_user_thread_url)

    if user_private_thread.first_post.id > other_user_private_thread.first_post.id:
        assert user_thread_index < other_user_thread_index
    else:
        assert other_user_thread_index < user_thread_index


def test_private_threads_search_view_shows_error_if_date_from_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem&date_from=invalid"
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, "Enter a valid date.")
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_uses_date_from_search_option(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    user_private_thread.started_at = user_private_thread.started_at.replace(
        year=2025, month=12, day=24
    )
    user_private_thread.save()

    user_private_thread.first_post.posted_at = (
        user_private_thread.first_post.posted_at.replace(year=2025, month=12, day=24)
    )
    user_private_thread.first_post.save()

    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem&date_from=2025-12-26"
    )

    assert_contains(response, "Search private threads")
    assert_not_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_contains(
        response,
        reverse(
            "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
        ),
    )
    assert_not_contains(response, "No private threads found")


@override_settings(MISAGO_THREADS_SEARCH={"RESULT_SIZE": 1})
def test_private_threads_search_view_keeps_date_from_in_more_url(
    user_client, user_private_thread, other_user_private_thread
):
    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem&date_from=2025-12-26"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:private-threads-search")
        + "?query=lorem&amp;mode=threads&amp;sort=relevance"
        + "&amp;date_from=2025-12-26",
    )


def test_private_threads_search_view_shows_error_if_date_to_is_invalid(user_client):
    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem&date_to=invalid"
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, "Enter a valid date.")
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_uses_date_to_search_option(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    today_date = date.today()

    user_private_thread.started_at += timedelta(days=5)
    user_private_thread.save()

    user_private_thread.first_post.posted_at += timedelta(days=5)
    user_private_thread.first_post.save()

    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + f"?query=lorem&date_to={today_date}"
    )

    assert_contains(response, "Search private threads")
    assert_not_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_contains(
        response,
        reverse(
            "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
        ),
    )
    assert_not_contains(response, "No private threads found")


@override_settings(MISAGO_THREADS_SEARCH={"RESULT_SIZE": 1})
def test_private_threads_search_view_keeps_date_to_in_more_url(
    user_client, user_private_thread, other_user_private_thread
):
    next_date = date.today() + timedelta(days=5)

    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + f"?query=lorem&date_to={next_date}"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:private-threads-search")
        + "?query=lorem&amp;mode=threads&amp;sort=relevance"
        + f"&amp;date_to={next_date}",
    )


def test_private_threads_search_view_swaps_date_from_and_date_to(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    date_from = date.today() + timedelta(days=2)
    date_to = date.today() - timedelta(days=2)

    user_private_thread.started_at -= timedelta(days=5)
    user_private_thread.save()

    user_private_thread.first_post.posted_at -= timedelta(days=5)
    user_private_thread.first_post.save()

    threads_search.bulk_index_threads([user_private_thread, other_user_private_thread])
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")
    threads_search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search")
        + f"?query=lorem&date_from={date_from}&date_to={date_to}"
    )

    assert_contains(response, "Search private threads")
    assert_not_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_contains(
        response,
        reverse(
            "misago:post", kwargs={"post_id": other_user_private_thread.first_post.id}
        ),
    )
    assert_not_contains(response, "No private threads found")


def test_private_threads_search_view_logs_user_search(
    user_client, user, user_private_thread
):
    threads_search.index_thread(user_private_thread)
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")

    search_log = SearchLog.objects.get(user=user)
    assert search_log.search_query == "lorem"
    assert search_log.ip_address
    assert not search_log.is_public


def test_private_threads_search_view_throttles_user_search(
    user_client, user, user_private_thread
):
    SearchLog.objects.create(
        user=user,
        ip_address="127.0.0.1",
        search_query="lorem",
    )

    threads_search.index_thread(user_private_thread)
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem"
    )

    assert_contains(response, "Search private threads")
    assert_not_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")
    assert_contains(response, "Search limit reached")


def test_private_threads_search_view_doesnt_throttle_user_with_permission(
    user_client, user, user_private_thread
):
    SearchLog.objects.create(
        user=user,
        ip_address="127.0.0.1",
        search_query="lorem",
    )

    user.group.bypass_search_throttling = True
    user.group.save()

    threads_search.index_thread(user_private_thread)
    threads_search.index_post(user_private_thread.first_post, "Lorem ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem"
    )

    assert_contains(response, "Search private threads")
    assert_contains(
        response,
        reverse("misago:post", kwargs={"post_id": user_private_thread.first_post.id}),
    )
    assert_not_contains(response, "No private threads found")
    assert_not_contains(response, "Search limit reached")
