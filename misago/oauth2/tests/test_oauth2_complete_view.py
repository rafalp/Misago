import responses
from django.contrib.auth import get_user_model
from django.urls import reverse
from responses.matchers import header_matcher, urlencoded_params_matcher

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ...users.bans import ban_ip
from ..client import SESSION_STATE
from ..models import Subject

User = get_user_model()


def test_oauth2_complete_view_returns_404_if_oauth_is_disabled(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is False

    response = client.get(reverse("misago:oauth2-complete"))
    assert response.status_code == 404


def test_oauth2_complete_view_returns_error_404_if_user_ip_is_banned_and_oauth_is_disabled(
    client, dynamic_settings
):
    ban_ip("127.*", "Ya got banned!")

    assert dynamic_settings.enable_oauth2_client is False

    response = client.get(reverse("misago:oauth2-complete"))
    assert response.status_code == 404


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_complete_view_returns_error_403_if_user_ip_is_banned(
    client, dynamic_settings
):
    ban_ip("127.*", "Ya got banned!")

    assert dynamic_settings.enable_oauth2_client is True

    response = client.get(reverse("misago:oauth2-complete"))
    assert_contains(response, "Ya got banned", 403)


TEST_SETTINGS = {
    "enable_oauth2_client": True,
    "oauth2_client_id": "oauth2_client_id",
    "oauth2_client_secret": "oauth2_client_secret",
    "oauth2_login_url": "https://example.com/oauth2/login",
    "oauth2_token_url": "https://example.com/oauth2/token",
    "oauth2_token_method": "POST",
    "oauth2_json_token_path": "token.bearer",
    "oauth2_user_url": "https://example.com/oauth2/user",
    "oauth2_user_method": "POST",
    "oauth2_user_token_name": "Authorization",
    "oauth2_user_token_location": "HEADER_BEARER",
    "oauth2_json_id_path": "id",
    "oauth2_json_name_path": "profile.name",
    "oauth2_json_email_path": "profile.email",
}


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_creates_new_user(client, dynamic_settings, mailoutbox):
    assert dynamic_settings.enable_oauth2_client is True

    code_grant = "12345grant"
    session_state = "12345state"
    access_token = "12345token"

    session = client.session
    session[SESSION_STATE] = session_state
    session.save()

    responses.post(
        "https://example.com/oauth2/token",
        json={
            "token": {
                "bearer": access_token,
            },
        },
        match=[
            urlencoded_params_matcher(
                {
                    "grant_type": "authorization_code",
                    "client_id": "oauth2_client_id",
                    "client_secret": "oauth2_client_secret",
                    "redirect_uri": "http://testserver/oauth2/complete/",
                    "code": code_grant,
                },
            ),
        ],
    )

    responses.post(
        "https://example.com/oauth2/user",
        json={
            "id": 1234,
            "profile": {
                "name": "John Doe",
                "email": "john@example.com",
            },
        },
        match=[
            header_matcher({"Authorization": f"Bearer {access_token}"}),
        ],
    )

    response = client.get(
        "%s?state=%s&code=%s"
        % (
            reverse("misago:oauth2-complete"),
            session_state,
            code_grant,
        )
    )

    assert response.status_code == 302

    # User and subject are created
    subject = Subject.objects.get(sub="1234")
    user = User.objects.get_by_email("john@example.com")
    assert subject.user_id == user.id

    assert user.username == "John_Doe"
    assert user.slug == "john-doe"
    assert user.email == "john@example.com"
    assert user.requires_activation == User.ACTIVATION_NONE

    # User is authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] == user.id

    # User welcome e-mail is sent
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Welcome on Misago forums!"


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_updates_existing_user(
    user, client, dynamic_settings, mailoutbox
):
    assert dynamic_settings.enable_oauth2_client is True

    Subject.objects.create(sub="1234", user=user)

    code_grant = "12345grant"
    session_state = "12345state"
    access_token = "12345token"

    session = client.session
    session[SESSION_STATE] = session_state
    session.save()

    responses.post(
        "https://example.com/oauth2/token",
        json={
            "token": {
                "bearer": access_token,
            },
        },
        match=[
            urlencoded_params_matcher(
                {
                    "grant_type": "authorization_code",
                    "client_id": "oauth2_client_id",
                    "client_secret": "oauth2_client_secret",
                    "redirect_uri": "http://testserver/oauth2/complete/",
                    "code": code_grant,
                },
            ),
        ],
    )

    responses.post(
        "https://example.com/oauth2/user",
        json={
            "id": 1234,
            "profile": {
                "name": "John Doe",
                "email": "john@example.com",
            },
        },
        match=[
            header_matcher({"Authorization": f"Bearer {access_token}"}),
        ],
    )

    response = client.get(
        "%s?state=%s&code=%s"
        % (
            reverse("misago:oauth2-complete"),
            session_state,
            code_grant,
        )
    )

    assert response.status_code == 302

    # User is updated
    user.refresh_from_db()
    assert user.username == "John_Doe"
    assert user.slug == "john-doe"
    assert user.email == "john@example.com"

    # User is authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] == user.id

    # User welcome e-mail is not sent
    assert len(mailoutbox) == 0


# TODO
# - session status is invalid or missing
# - code grant is invalid
# - user data didn't validate
# - deactivated user account update
# - banned user account create
# - banned user account update