from django.urls import reverse


def test_formatting_help_view_renders_page(db, client):
    response = client.get(reverse("misago:formatting-help"))
    assert response.status_code == 200


def test_formatting_help_view_renders_page_for_authenticated_user(user_client):
    response = user_client.get(reverse("misago:formatting-help"))
    assert response.status_code == 200


def test_formatting_help_view_renders_in_html(db, client):
    response = client.get(
        reverse("misago:formatting-help"),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200


def test_formatting_help_view_renders_in_html_for_authenticated_user(user_client):
    response = user_client.get(
        reverse("misago:formatting-help"),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200
