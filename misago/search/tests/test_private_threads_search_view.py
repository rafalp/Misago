from django.test import override_settings
from django.urls import reverse

from ...privatethreads.models import PrivateThreadMember
from ...test import assert_contains, assert_not_contains
from ..enums import SearchMode
from ..models import SearchLog
from ..service import search


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
    search.index_thread(user_private_thread)
    search.index_post(
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
    search.index_thread(user_private_thread)
    search.index_post(user_private_thread.first_post, "Content")

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
    search.index_thread(user_private_thread)
    search.index_post(
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

    search.index_thread(private_thread)
    search.index_post(private_thread.first_post, private_thread.first_post.content)

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

    search.index_thread(private_thread)
    search.index_post(private_thread.first_post, "Content")

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

    search.index_thread(private_thread)
    search.index_post(private_thread.first_post, private_thread.first_post.content)

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
    search.index_thread(user_private_thread)
    search.index_post(
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


@override_settings(MISAGO_SEARCH={"RESULT_SIZE": 1})
def test_private_threads_search_view_shows_results_with_next_page(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    search.bulk_index_threads([user_private_thread, other_user_private_thread])
    search.index_post(user_private_thread.first_post, "Lorem ipsum")
    search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

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
    search.bulk_index_threads([user_private_thread, other_user_private_thread])
    search.index_post(user_private_thread.first_post, "Lorem ipsum")
    search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

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
    search.bulk_index_threads([user_private_thread, other_user_private_thread])
    search.index_post(user_private_thread.first_post, "Lorem ipsum")
    search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

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


@override_settings(MISAGO_SEARCH={"RESULT_SIZE": 1})
def test_private_threads_search_view_keeps_search_query_in_more_url(
    user_client,
    user_private_thread,
    other_user_private_thread,
):
    search.bulk_index_threads([user_private_thread, other_user_private_thread])
    search.index_post(user_private_thread.first_post, "Lorem ipsum")
    search.index_post(other_user_private_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:private-threads-search") + "?query=lorem"
    )

    assert_contains(response, "Search private threads")
    assert_contains(response, reverse("misago:private-threads-search") + "?query=lorem")


def test_private_threads_search_view_logs_user_search(
    user_client, user, user_private_thread
):
    search.index_thread(user_private_thread)
    search.index_post(user_private_thread.first_post, "Lorem ipsum")

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

    search.index_thread(user_private_thread)
    search.index_post(user_private_thread.first_post, "Lorem ipsum")

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

    search.index_thread(user_private_thread)
    search.index_post(user_private_thread.first_post, "Lorem ipsum")

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
