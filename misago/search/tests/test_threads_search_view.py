from django.test import override_settings
from django.urls import reverse

from ...test import assert_contains, assert_not_contains
from ..enums import SearchMode
from ..service import search


def test_threads_search_view_returns_error_403_if_user_cant_search(user_client, user):
    user.group.can_search = False
    user.group.save()

    response = user_client.get(reverse("misago:threads-search"))
    assert_contains(response, "You can&#x27;t search this site.", status_code=403)


def test_threads_search_view_shows_user_threads_result(user_client, user_thread):
    search.index_thread(user_thread)
    search.index_post(user_thread.first_post, user_thread.first_post.content)

    response = user_client.get(reverse("misago:threads-search") + "?query=Thread")

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": user_thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_user_posts_result(user_client, user_thread):
    search.index_thread(user_thread)
    search.index_post(user_thread.first_post, "Content")

    response = user_client.get(
        reverse("misago:threads-search") + f"?query=Content&mode={SearchMode.POSTS}"
    )

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": user_thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_user_thread_titles_result(user_client, user_thread):
    search.index_thread(user_thread)
    search.index_post(user_thread.first_post, user_thread.first_post.content)

    response = user_client.get(
        reverse("misago:threads-search")
        + f"?query=Thread&mode={SearchMode.THREAD_TITLES}"
    )

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": user_thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_deleted_user_threads_result(user_client, thread):
    search.index_thread(thread)
    search.index_post(thread.first_post, thread.first_post.content)

    response = user_client.get(reverse("misago:threads-search") + "?query=Thread")

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_deleted_user_posts_result(user_client, thread):
    search.index_thread(thread)
    search.index_post(thread.first_post, "Content")

    response = user_client.get(
        reverse("misago:threads-search") + f"?query=Content&mode={SearchMode.POSTS}"
    )

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_deleted_user_thread_titles_result(
    user_client, thread
):
    search.index_thread(thread)
    search.index_post(thread.first_post, thread.first_post.content)

    response = user_client.get(
        reverse("misago:threads-search")
        + f"?query=Thread&mode={SearchMode.THREAD_TITLES}"
    )

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_result_in_htmx(user_client, user_thread):
    search.index_thread(user_thread)
    search.index_post(user_thread.first_post, user_thread.first_post.content)

    response = user_client.get(
        reverse("misago:threads-search") + "?query=Thread",
        headers={"hx-request": "true"},
    )

    assert_not_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": user_thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_no_results_page(user_client):
    response = user_client.get(reverse("misago:threads-search") + "?query=test")

    assert_contains(response, "Search threads")
    assert_contains(response, "No threads found")


def test_threads_search_view_shows_no_results_page_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test", headers={"hx-request": "true"}
    )

    assert_not_contains(response, "Search threads")
    assert_contains(response, "No threads found")


def test_threads_search_view_shows_no_results_page_for_offset(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=10"
    )

    assert_contains(response, "Search threads")
    assert_contains(response, "No threads found")


def test_threads_search_view_shows_no_results_page_for_offset_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=10",
        headers={"hx-request": "true"},
    )

    assert_not_contains(response, "Search threads")
    assert_contains(response, "No threads found")


def test_threads_search_view_returns_404_for_invalid_offset(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=invalid"
    )
    assert response.status_code == 404


def test_threads_search_view_returns_404_for_invalid_offset_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=invalid",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_threads_search_view_returns_404_for_negative_offset(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=-1"
    )
    assert response.status_code == 404


def test_threads_search_view_returns_404_for_negative_offset_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=-1",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


def test_threads_search_view_returns_404_for_max_offset(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=1000"
    )
    assert response.status_code == 404


def test_threads_search_view_returns_404_for_max_offset_in_htmx(user_client):
    response = user_client.get(
        reverse("misago:threads-search") + "?query=test&offset=1000",
        headers={"hx-request": "true"},
    )
    assert response.status_code == 404


@override_settings(MISAGO_SEARCH={"RESULT_SIZE": 1})
def test_threads_search_view_shows_results_with_next_page(
    user_client, thread, user_thread
):
    search.bulk_index_threads([thread, user_thread])
    search.index_post(thread.first_post, "Lorem ipsum")
    search.index_post(user_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(reverse("misago:threads-search") + "?query=lorem ipsum")

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": thread.first_post.id})
    )
    assert_not_contains(
        response, reverse("misago:post", kwargs={"post_id": user_thread.first_post.id})
    )
    assert_contains(response, "Load more")
    assert_contains(
        response,
        reverse("misago:threads-search")
        + "?query=lorem+ipsum&amp;mode=threads&amp;sort=relevance&amp;offset=1",
    )
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_results_without_next_page(
    user_client, thread, user_thread
):
    search.bulk_index_threads([thread, user_thread])
    search.index_post(thread.first_post, "Lorem ipsum")
    search.index_post(user_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(reverse("misago:threads-search") + "?query=lorem ipsum")

    assert_contains(response, "Search threads")
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": thread.first_post.id})
    )
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": user_thread.first_post.id})
    )
    assert_not_contains(response, "Load more")
    assert_not_contains(response, "offset=")
    assert_not_contains(response, "No threads found")


def test_threads_search_view_shows_results_after_offset(
    user_client, thread, user_thread
):
    search.bulk_index_threads([thread, user_thread])
    search.index_post(thread.first_post, "Lorem ipsum")
    search.index_post(user_thread.first_post, "Lorem latin ipsum")

    response = user_client.get(
        reverse("misago:threads-search") + "?query=lorem ipsum&offset=1"
    )

    assert_contains(response, "Search threads")
    assert_not_contains(
        response, reverse("misago:post", kwargs={"post_id": thread.first_post.id})
    )
    assert_contains(
        response, reverse("misago:post", kwargs={"post_id": user_thread.first_post.id})
    )
    assert_not_contains(response, "No threads found")
