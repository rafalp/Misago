from django.urls import reverse

from ...test import assert_contains


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
