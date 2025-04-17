import json

from django.urls import reverse

view_url = reverse("misago:suggest-users")


def test_suggest_users_view_returns_empty_suggestions_for_anonymous_user(client, user):
    response = client.get(view_url + "?q=bob")
    assert response.status_code == 200
    assert not json.loads(response.content)["results"]


def test_suggest_users_view_returns_suggestions_for_anonymous_user(client, user):
    response = client.get(view_url + "?q=use")
    assert response.status_code == 200
    assert json.loads(response.content)["results"]


def test_suggest_users_view_returns_exact_suggestion_for_anonymous_user(client, user):
    response = client.get(view_url + "?q=user")
    assert response.status_code == 200
    assert json.loads(response.content)["results"]


def test_suggest_users_view_returns_suggestions_for_authenticated_user(
    user_client, other_user
):
    response = user_client.get(view_url + f"?q=other")
    assert response.status_code == 200
    assert json.loads(response.content)["results"]


def test_suggest_users_view_returns_empty_suggestions_for_authenticated_user(
    user_client,
):
    response = user_client.get(view_url + f"?q=bob")
    assert response.status_code == 200
    assert not json.loads(response.content)["results"]


def test_suggest_users_view_returns_exact_suggestion_for_authenticated_user(
    user_client, other_user
):
    response = user_client.get(view_url + "?q=other_user")
    assert response.status_code == 200
    assert json.loads(response.content)["results"]


def test_suggest_users_view_returns_exact_self_suggestion_for_authenticated_user(
    user_client,
):
    response = user_client.get(view_url + "?q=user")
    assert response.status_code == 200
    assert json.loads(response.content)["results"]
