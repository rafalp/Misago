from django.urls import reverse

from ..users import search_users


def test_search_users_returns_no_results(
    user_permissions_factory, admin, moderator, user, other_user
):
    user_permissions = user_permissions_factory(user)
    results = search_users(user_permissions, "invalid")

    assert results == []


def test_search_users_returns_exact_match_user(
    user_permissions_factory, admin, moderator, user, other_user
):
    user_permissions = user_permissions_factory(user)
    results = search_users(user_permissions, admin.username)

    assert results == [admin]


def test_search_users_excludes_searcher(
    user_permissions_factory, admin, moderator, user, other_user
):
    user_permissions = user_permissions_factory(user)
    results = search_users(user_permissions, user.username)

    assert results == []


def test_search_users_includes_searcher_when_enabled(
    user_permissions_factory, admin, moderator, user, other_user
):
    user_permissions = user_permissions_factory(user)
    results = search_users(user_permissions, user.username, include_self=True)

    assert results == [user]


def test_search_users_does_simple_fuzzy_search(
    user_permissions_factory, admin, moderator, user, other_user
):
    user_permissions = user_permissions_factory(user)
    results = search_users(user_permissions, "otherusr")

    assert results == [other_user]


def test_search_users_excludes_inactive_users(
    user_permissions_factory, user, inactive_user
):
    user_permissions = user_permissions_factory(user)
    results = search_users(user_permissions, inactive_user.username)

    assert results == []


def test_search_users_includes_inactive_users_when_enabled(
    user_permissions_factory, user, inactive_user
):
    user_permissions = user_permissions_factory(user)
    results = search_users(
        user_permissions, inactive_user.username, include_deactivated=True
    )

    assert results == [inactive_user]
