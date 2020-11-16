from django.urls import reverse

api_link = reverse("misago:api:parse-markup")


def test_api_rejects_unauthenticated_user(db, client):
    response = client.post(api_link)
    assert response.status_code == 403


def test_api_rejects_request_without_data(user_client):
    response = user_client.post(api_link)
    assert response.status_code == 400
    assert response.json() == {"detail": "You have to enter a message."}


def test_api_rejects_request_with_invalid_shaped_data(user_client):
    response = user_client.post(api_link, "[]", content_type="application/json")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid data. Expected a dictionary, but got list."
    }

    response = user_client.post(api_link, "123", content_type="application/json")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid data. Expected a dictionary, but got int."
    }

    response = user_client.post(api_link, '"string"', content_type="application/json")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid data. Expected a dictionary, but got str."
    }


def test_api_rejects_request_with_malformed_data(user_client):
    response = user_client.post(api_link, "malformed", content_type="application/json")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"
    }


def test_api_validates_that_post_has_content(user_client):
    response = user_client.post(api_link, json={"post": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "You have to enter a message."}


# regression test for #929
def test_api_strips_whitespace_from_post_before_validating_length(user_client):
    response = user_client.post(api_link, json={"post": "\n"})
    assert response.status_code == 400
    assert response.json() == {"detail": "You have to enter a message."}


def test_api_casts_post_value_to_string(user_client):
    response = user_client.post(api_link, json={"post": 123})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Posted message should be at least 5 characters long (it has 3)."
    }


def test_api_returns_parsed_value(user_client):
    response = user_client.post(api_link, json={"post": "Hello world!"})
    assert response.status_code == 200
    assert response.json() == {"parsed": "<p>Hello world!</p>"}
