import responses
from django.contrib.auth import get_user_model
from django.urls import reverse
from responses.matchers import header_matcher, urlencoded_params_matcher

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ...users.bans import ban_ip, ban_user
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


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_complete_view_returns_error_400_if_user_canceled_sign_in(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is True

    response = client.get("%s?error=access_denied" % reverse("misago:oauth2-complete"))
    assert_contains(response, "The OAuth2 process was canceled by the provider.", 400)


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_complete_view_returns_error_400_if_state_is_not_set(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is True

    response = client.get(reverse("misago:oauth2-complete"))
    assert_contains(response, "OAuth2 session is missing state.", 400)


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_complete_view_returns_error_400_if_state_is_invalid(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is True

    session = client.session
    session[SESSION_STATE] = "state123"
    session.save()

    response = client.get(
        "%s?state=invalid&code=1234" % reverse("misago:oauth2-complete")
    )
    assert_contains(
        response,
        "OAuth2 state sent by the provider did not match one in the session.",
        400,
    )


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_scopes="scopes",
    oauth2_login_url="https://example.com/oauth2/login",
)
def test_oauth2_complete_view_returns_error_400_if_code_is_missing(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is True

    session = client.session
    session[SESSION_STATE] = "state123"
    session.save()

    response = client.get("%s?state=state123&code=" % reverse("misago:oauth2-complete"))
    assert_contains(
        response,
        "OAuth2 authorization code was not sent by the provider.",
        400,
    )


TEST_SETTINGS = {
    "enable_oauth2_client": True,
    "oauth2_client_id": "oauth2_client_id",
    "oauth2_client_secret": "oauth2_client_secret",
    "oauth2_login_url": "https://example.com/oauth2/login",
    "oauth2_token_url": "https://example.com/oauth2/token",
    "oauth2_json_token_path": "token.bearer",
    "oauth2_user_url": "https://example.com/oauth2/user",
    "oauth2_user_method": "POST",
    "oauth2_user_token_name": "Authorization",
    "oauth2_user_token_location": "HEADER_BEARER",
    "oauth2_send_welcome_email": True,
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


TEST_SETTINGS_EMAIL_DISABLED = TEST_SETTINGS.copy()
TEST_SETTINGS_EMAIL_DISABLED["oauth2_send_welcome_email"] = False


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS_EMAIL_DISABLED)
def test_oauth2_complete_view_doesnt_send_welcome_mail_if_option_is_disabled(
    client, dynamic_settings, mailoutbox
):
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

    # User is authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] == user.id

    # User welcome e-mail is not sent
    assert len(mailoutbox) == 0


TEST_SETTINGS_EXTRA_TOKEN_HEADERS = TEST_SETTINGS.copy()
TEST_SETTINGS_EXTRA_TOKEN_HEADERS["oauth2_token_extra_headers"] = (
    """
Accept: application/json
API-Version: 2.1.3.7
""".strip()
)


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS_EXTRA_TOKEN_HEADERS)
def test_oauth2_complete_view_includes_extra_headers_in_token_request(
    client, dynamic_settings, mailoutbox
):
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
            header_matcher(
                {
                    "Accept": "application/json",
                    "API-Version": "2.1.3.7",
                }
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

    # User is authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] == user.id


TEST_SETTINGS_EXTRA_USER_HEADERS = TEST_SETTINGS.copy()
TEST_SETTINGS_EXTRA_USER_HEADERS["oauth2_user_extra_headers"] = (
    """
X-Header: its-a-test
API-Version: 2.1.3.7
""".strip()
)


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS_EXTRA_USER_HEADERS)
def test_oauth2_complete_view_includes_extra_headers_in_user_request(
    client, dynamic_settings, mailoutbox
):
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
            header_matcher(
                {
                    "Authorization": f"Bearer {access_token}",
                    "X-Header": "its-a-test",
                    "API-Version": "2.1.3.7",
                }
            ),
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

    # User is authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] == user.id


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


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_returns_error_400_if_code_grant_is_rejected(
    client, dynamic_settings
):
    assert dynamic_settings.enable_oauth2_client is True

    code_grant = "12345grant"
    session_state = "12345state"

    session = client.session
    session[SESSION_STATE] = session_state
    session.save()

    responses.post(
        "https://example.com/oauth2/token",
        json={
            "error": "Permission denied",
        },
        status=403,
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

    response = client.get(
        "%s?state=%s&code=%s"
        % (
            reverse("misago:oauth2-complete"),
            session_state,
            code_grant,
        )
    )

    assert_contains(
        response,
        "The OAuth2 provider responded with error for an access token request.",
        400,
    )


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_returns_error_400_if_access_token_is_rejected(
    user, client, dynamic_settings
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
            "error": "Permission denied",
        },
        status=403,
    )

    response = client.get(
        "%s?state=%s&code=%s"
        % (
            reverse("misago:oauth2-complete"),
            session_state,
            code_grant,
        )
    )

    assert_contains(
        response,
        "The OAuth2 provider responded with error for user profile request.",
        400,
    )


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_returns_error_400_if_user_email_was_missing(
    user, client, dynamic_settings
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

    assert_contains(response, "Enter a valid e-mail address.", 400)


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_returns_error_400_if_user_email_was_invalid(
    user, client, dynamic_settings
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
                "email": "invalid",
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

    assert_contains(response, "Enter a valid e-mail address.", 400)


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_returns_error_400_if_user_data_causes_integrity_error(
    user, client, dynamic_settings
):
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
                "email": user.email,
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

    assert_contains(
        response,
        (
            "Your e-mail address returned by the provider is not available "
            "for use on this site."
        ),
        400,
    )


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_updates_deactivated_user_but_returns_error_400(
    inactive_user, client, dynamic_settings, mailoutbox
):
    assert dynamic_settings.enable_oauth2_client is True

    Subject.objects.create(sub="1234", user=inactive_user)

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

    assert_contains(
        response,
        (
            "User account associated with the profile from the OAuth2 provider "
            "was deactivated by the site administrator."
        ),
        400,
    )

    # User is updated but still deactivated
    inactive_user.refresh_from_db()
    assert inactive_user.username == "John_Doe"
    assert inactive_user.slug == "john-doe"
    assert inactive_user.email == "john@example.com"
    assert inactive_user.is_active is False

    # User is not authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] is None

    # User welcome e-mail is not sent
    assert len(mailoutbox) == 0


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_creates_banned_user_but_returns_error_403(
    user, client, dynamic_settings, mailoutbox
):
    assert dynamic_settings.enable_oauth2_client is True

    user.username = "John_Doe"
    ban_user(user, "Banned for a test.")
    user.refresh_from_db()

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

    assert_contains(response, "Banned for a test.", 403)

    # User is created
    new_user = User.objects.get_by_email("john@example.com")
    assert new_user
    assert new_user.id != user.id
    assert new_user.username == "John_Doe"
    assert new_user.slug == "john-doe"
    assert new_user.email == "john@example.com"

    # User is not authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] is None

    # User welcome e-mail is not sent
    assert len(mailoutbox) == 0


@responses.activate
@override_dynamic_settings(**TEST_SETTINGS)
def test_oauth2_complete_view_updates_banned_user_but_returns_error_403(
    user, client, dynamic_settings, mailoutbox
):
    assert dynamic_settings.enable_oauth2_client is True

    Subject.objects.create(sub="1234", user=user)

    user.username = "John_Doe"
    ban_user(user, "Banned for a test.")
    user.refresh_from_db()

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

    assert_contains(response, "Banned for a test.", 403)

    # User is updated
    user.refresh_from_db()
    assert user.username == "John_Doe"
    assert user.slug == "john-doe"
    assert user.email == "john@example.com"

    # User is not authenticated
    auth_api = client.get(reverse("misago:api:auth")).json()
    assert auth_api["id"] is None

    # User welcome e-mail is not sent
    assert len(mailoutbox) == 0
