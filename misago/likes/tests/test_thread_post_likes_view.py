from django.urls import reverse

from ...permissions.enums import CanSeePostLikes
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ..like import like_post


def test_thread_post_likes_view_shows_empty(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "This post has no likes.")


def test_thread_post_likes_view_shows_empty_to_anonymous_user(client, thread, post):
    response = client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "This post has no likes.")


def test_thread_post_likes_view_shows_empty_in_htmx(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no likes.")


def test_thread_post_likes_view_shows_empty_to_anonymous_user_in_htmx(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no likes.")


def test_thread_post_likes_view_shows_empty_in_modal(user_client, thread, post):
    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no likes.")


def test_thread_post_likes_view_shows_empty_to_anonymous_user_in_modal(
    client, thread, post
):
    response = client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "This post has no likes.")


def test_thread_post_likes_view_shows_user_like(user_client, other_user, thread, post):
    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, other_user.username)


def test_thread_post_likes_view_shows_deleted_user_like(user_client, thread, post):
    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert_contains(response, "DeletedUser")


def test_thread_post_likes_view_shows_user_like_in_modal(
    user_client, other_user, thread, post
):
    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user.username)


def test_thread_post_likes_view_shows_deleted_user_like_in_modal(
    user_client, thread, post
):
    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_contains(response, "DeletedUser")


def test_thread_post_likes_view_displays_another_page_of_results(
    user_client, thread, post
):
    for i in range(1, 41):
        like_post(post, f"User{i}")

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
    )
    assert_not_contains(response, "User40")
    assert_contains(response, "User1")


def test_thread_post_likes_view_displays_another_page_of_results_in_htmx(
    user_client, thread, post
):
    for i in range(1, 41):
        like_post(post, f"User{i}")

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "User40")
    assert_contains(response, "User1")


def test_thread_post_likes_view_displays_another_page_of_results_in_modal(
    user_client, thread, post
):
    for i in range(1, 20):
        like_post(post, f"User{i}")

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 2,
            },
        )
        + "?modal=true",
        headers={"hx-request": "true"},
    )
    assert_not_contains(response, "User10")
    assert_contains(response, "User1")


def test_thread_post_likes_view_redirects_from_out_of_range_last_page(
    user_client, thread, post
):
    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 3,
            },
        )
    )

    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread-post-likes",
        kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
    )


def test_thread_post_likes_view_displays_last_page_from_out_of_range_last_page_in_htmx(
    user_client, thread, post
):
    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
                "page": 3,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, "DeletedUser")


def test_thread_post_likes_view_returns_error_404_if_thread_doesnt_exist(user_client):
    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": 100, "slug": "not-found", "post_id": 1},
        )
    )
    assert response.status_code == 404


def test_thread_post_likes_view_returns_error_404_if_thread_post_doesnt_exist(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": thread.last_post_id + 1,
            },
        )
    )
    assert response.status_code == 404


def test_thread_post_likes_view_returns_error_404_if_post_doesnt_exist_in_thread(
    user_client, thread, user_thread
):
    post = user_thread.first_post

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404


def test_thread_post_likes_view_returns_error_404_if_user_has_no_category_permission(
    user_client, thread, post
):
    CategoryGroupPermission.objects.filter(category=thread.category).delete()

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404


def test_thread_post_likes_view_returns_error_404_if_user_has_no_thread_permission(
    user_client, thread, post
):
    thread.is_unapproved = True
    thread.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404


def test_thread_post_likes_view_returns_error_404_if_user_has_no_post_permission(
    user_client, thread, post
):
    post.is_unapproved = True
    post.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "post_id": post.id},
        )
    )
    assert response.status_code == 404


def test_thread_post_likes_view_returns_error_403_if_user_cant_see_posts_likes(
    user_client, members_group, thread, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(
        response, "You can&#x27;t see this post&#x27;s likes.", status_code=403
    )


def test_thread_post_likes_view_returns_error_403_if_user_can_see_posts_likes_count_only(
    user_client, members_group, thread, post
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "post_id": post.id,
            },
        ),
    )
    assert_contains(
        response, "You can&#x27;t see this post&#x27;s likes.", status_code=403
    )


def test_thread_post_likes_view_returns_error_404_if_post_is_in_private_thread(
    user_client, user_private_thread
):
    post = user_private_thread.first_post

    response = user_client.get(
        reverse(
            "misago:thread-post-likes",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        )
    )
    assert response.status_code == 404
