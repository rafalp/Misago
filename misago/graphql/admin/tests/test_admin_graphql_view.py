from django.test import Client

from ....test import assert_contains


def test_admin_graphql_renders_playground_on_get(admin_client, admin_graphql_link):
    response = admin_client.get(admin_graphql_link)
    assert response.status_code == 200


def test_admin_graphql_server_returns_bad_request_if_post_request_was_not_json(
    admin_client, admin_graphql_link
):
    response = admin_client.post(admin_graphql_link)
    assert response.status_code == 400


def test_admin_graphql_server_returns_bad_request_if_post_request_was_invalid_json(
    admin_client, admin_graphql_link
):
    response = admin_client.post(
        admin_graphql_link, data="invalid", content_type="application/json"
    )
    assert response.status_code == 400


def test_admin_graphql_server_returns_bad_request_if_request_method_was_put(
    admin_client, admin_graphql_link
):
    response = admin_client.put(admin_graphql_link)
    assert response.status_code == 400


def test_admin_graphql_server_returns_bad_request_if_request_method_was_patch(
    admin_client, admin_graphql_link
):
    response = admin_client.patch(admin_graphql_link)
    assert response.status_code == 400


def test_admin_graphql_server_returns_bad_request_if_request_method_was_delete(
    admin_client, admin_graphql_link
):
    response = admin_client.delete(admin_graphql_link)
    assert response.status_code == 400


def test_admin_graphql_server_requires_authentication_to_use_playground(
    db, client, admin_graphql_link
):
    response = client.get(admin_graphql_link)
    assert_contains(response, "Sign in")


def test_admin_graphql_server_requires_authentication_to_run_query(
    db, client, admin_graphql_link
):
    response = client.post(
        admin_graphql_link,
        data='{"query": "{ test }"}',
        content_type="application/json",
    )
    assert_contains(response, "Sign in")


def test_admin_graphql_server_handles_csrf_error_for_post_request_without_auth(
    db, admin_graphql_link
):
    client = Client(enforce_csrf_checks=True)
    response = client.post(
        admin_graphql_link,
        data='{"query": "{ test }"}',
        content_type="application/json",
    )
    assert_contains(response, "Form submission rejected", status_code=403)
