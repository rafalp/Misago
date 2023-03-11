from django.urls import reverse

from ...test import assert_contains, assert_not_contains


def test_body_has_misago_anonymous_css_class_if_user_is_anonymous(db, client):
    response = client.get(reverse("misago:index"))
    assert_contains(response, 'class="misago-anonymous')
    assert_not_contains(response, 'class="misago-authenticated')


def test_body_has_misago_authenticated_css_class_if_user_is_authenticated(user_client):
    response = user_client.get(reverse("misago:index"))
    assert_contains(response, 'class="misago-authenticated')
    assert_not_contains(response, 'class="misago-anonymous')
