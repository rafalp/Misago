from django.urls import reverse
from ...models import Setting
from ....test import assert_contains, assert_has_error_message


def test_oauth2_can_be_enabled(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "1",
            "oauth2_provider": "Lorem",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_enable_pkce": "0",
            "oauth2_pkce_code_challenge_method": "S256",
            "oauth2_scopes": "some scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": "",
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "avatar",
        },
    )

    assert response.status_code == 302

    settings = {row.setting: row.value for row in Setting.objects.all()}

    assert settings["enable_oauth2_client"] is True
    assert settings["oauth2_provider"] == "Lorem"
    assert settings["oauth2_client_id"] == "id"
    assert settings["oauth2_client_secret"] == "secret"
    assert settings["oauth2_enable_pkce"] is False
    assert settings["oauth2_pkce_code_challenge_method"] == "S256"
    assert settings["oauth2_scopes"] == "some scope"
    assert settings["oauth2_login_url"] == "https://example.com/login/"
    assert settings["oauth2_token_url"] == "https://example.com/token/"
    assert settings["oauth2_token_extra_headers"] == ""
    assert settings["oauth2_json_token_path"] == "access_token"
    assert settings["oauth2_user_url"] == "https://example.com/user/"
    assert settings["oauth2_user_method"] == "GET"
    assert settings["oauth2_user_token_location"] == "HEADER"
    assert settings["oauth2_user_token_name"] == "access_token"
    assert settings["oauth2_user_extra_headers"] == ""
    assert settings["oauth2_send_welcome_email"] is False
    assert settings["oauth2_json_id_path"] == "id"
    assert settings["oauth2_json_name_path"] == "name"
    assert settings["oauth2_json_email_path"] == "email"
    assert settings["oauth2_json_avatar_path"] == "avatar"


def test_oauth2_can_be_enabled_without_avatar(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "1",
            "oauth2_provider": "Lorem",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_enable_pkce": "0",
            "oauth2_pkce_code_challenge_method": "S256",
            "oauth2_scopes": "some scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": "",
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert response.status_code == 302

    settings = {row.setting: row.value for row in Setting.objects.all()}

    assert settings["enable_oauth2_client"] is True
    assert settings["oauth2_provider"] == "Lorem"
    assert settings["oauth2_client_id"] == "id"
    assert settings["oauth2_client_secret"] == "secret"
    assert settings["oauth2_enable_pkce"] is False
    assert settings["oauth2_pkce_code_challenge_method"] == "S256"
    assert settings["oauth2_scopes"] == "some scope"
    assert settings["oauth2_login_url"] == "https://example.com/login/"
    assert settings["oauth2_token_url"] == "https://example.com/token/"
    assert settings["oauth2_token_extra_headers"] == ""
    assert settings["oauth2_json_token_path"] == "access_token"
    assert settings["oauth2_user_url"] == "https://example.com/user/"
    assert settings["oauth2_user_method"] == "GET"
    assert settings["oauth2_user_token_location"] == "HEADER"
    assert settings["oauth2_user_token_name"] == "access_token"
    assert settings["oauth2_user_extra_headers"] == ""
    assert settings["oauth2_send_welcome_email"] is False
    assert settings["oauth2_json_id_path"] == "id"
    assert settings["oauth2_json_name_path"] == "name"
    assert settings["oauth2_json_email_path"] == "email"
    assert settings["oauth2_json_avatar_path"] == ""


def test_oauth2_cant_be_enabled_with_some_value_missing(admin_client):
    data = {
        "enable_oauth2_client": "1",
        "oauth2_provider": "Lorem",
        "oauth2_client_id": "id",
        "oauth2_client_secret": "secret",
        "oauth2_enable_pkce": "0",
        "oauth2_pkce_code_challenge_method": "S256",
        "oauth2_scopes": "some scope",
        "oauth2_login_url": "https://example.com/login/",
        "oauth2_token_url": "https://example.com/token/",
        "oauth2_token_extra_headers": "",
        "oauth2_json_token_path": "access_token",
        "oauth2_user_url": "https://example.com/user/",
        "oauth2_user_method": "GET",
        "oauth2_user_token_location": "HEADER",
        "oauth2_user_token_name": "access_token",
        "oauth2_user_extra_headers": "",
        "oauth2_send_welcome_email": "",
        "oauth2_json_id_path": "id",
        "oauth2_json_name_path": "name",
        "oauth2_json_email_path": "email",
        "oauth2_json_avatar_path": "",
    }

    skip_settings = (
        "enable_oauth2_client",
        "oauth2_enable_pkce",
        "oauth2_pkce_code_challenge_method",
        "oauth2_json_avatar_path",
        "oauth2_token_extra_headers",
        "oauth2_user_method",
        "oauth2_user_token_location",
        "oauth2_user_extra_headers",
        "oauth2_send_welcome_email",
    )

    for setting in data:
        if setting in skip_settings:
            continue

        new_data = data.copy()
        new_data[setting] = ""

        response = admin_client.post(
            reverse("misago:admin:settings:oauth2:index"),
            new_data,
        )

        assert response.status_code == 302
        assert_has_error_message(
            response,
            "You need to complete the configuration before you will be able to enable OAuth 2 on your site.",
        )

        settings = {row.setting: row.value for row in Setting.objects.all()}

        assert settings["enable_oauth2_client"] is False

        if setting != "oauth2_client_id":
            assert settings["oauth2_client_id"] == "id"

        if setting != "oauth2_client_secret":
            assert settings["oauth2_client_secret"] == "secret"

        if setting != "oauth2_scopes":
            assert settings["oauth2_scopes"] == "some scope"

        if setting != "oauth2_login_url":
            assert settings["oauth2_login_url"] == "https://example.com/login/"

        if setting != "oauth2_token_url":
            assert settings["oauth2_token_url"] == "https://example.com/token/"

        if setting != "oauth2_json_token_path":
            assert settings["oauth2_json_token_path"] == "access_token"

        if setting != "oauth2_user_url":
            assert settings["oauth2_user_url"] == "https://example.com/user/"

        if setting != "oauth2_user_token_name":
            assert settings["oauth2_user_token_name"] == "access_token"

        if setting != "oauth2_json_id_path":
            assert settings["oauth2_json_id_path"] == "id"

        if setting != "oauth2_json_name_path":
            assert settings["oauth2_json_name_path"] == "name"

        if setting != "oauth2_json_email_path":
            assert settings["oauth2_json_email_path"] == "email"


def test_oauth2_scopes_are_normalized(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_enable_pkce": "0",
            "oauth2_pkce_code_challenge_method": "S256",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert response.status_code == 302

    setting = Setting.objects.get(setting="oauth2_scopes")
    assert setting.value == "some scope"


def test_oauth2_extra_token_headers_are_normalized(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_enable_pkce": "0",
            "oauth2_pkce_code_challenge_method": "S256",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": ("Lorem:   ipsum\n   Dolor: Met-elit"),
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": "",
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert response.status_code == 302

    setting = Setting.objects.get(setting="oauth2_token_extra_headers")
    assert setting.value == "Lorem: ipsum\nDolor: Met-elit"


def test_oauth2_extra_token_headers_are_validated(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": (
                "Lorem:   ipsum\n   Dolor-amet\n Dolor: Met-elit"
            ),
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": "",
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert_contains(response, "is not a valid header")


def test_oauth2_extra_user_headers_are_normalized(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_enable_pkce": "0",
            "oauth2_pkce_code_challenge_method": "S256",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": ("Lorem:   ipsum\n   Dolor: Met-amet"),
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert response.status_code == 302

    setting = Setting.objects.get(setting="oauth2_user_extra_headers")
    assert setting.value == "Lorem: ipsum\nDolor: Met-amet"


def test_oauth2_extra_user_headers_are_validated(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": ("Lorem:   ipsum\n   Dolor-met"),
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert_contains(response, "is not a valid header")


def test_oauth2_extra_headers_are_validated_to_have_colons(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": ("Lorem:   ipsum\n   Dolor-met"),
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert_contains(response, "is not a valid header. It&#x27;s missing a colon")


def test_oauth2_extra_headers_are_validated_to_have_names(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": ("Lorem:   ipsum\n   :Dolor-met"),
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert_contains(
        response,
        "is not a valid header. It&#x27;s missing a header name before the colon",
    )


def test_oauth2_extra_headers_are_validated_to_have_values(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": ("Lorem:   ipsum\n   Dolor-met:"),
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert_contains(
        response,
        "is not a valid header. It&#x27;s missing a header value after the colon",
    )


def test_oauth2_extra_headers_are_validated_to_be_unique(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "0",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_scopes": "some some    scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": ("Accept:b\nLorem:   ipsum\n   Accept: a"),
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "",
        },
    )

    assert_contains(response, "&quot;Accept&quot; header is entered more than once.")


def test_oauth2_can_be_enabled_with_pkce(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:oauth2:index"),
        {
            "enable_oauth2_client": "1",
            "oauth2_provider": "Lorem",
            "oauth2_client_id": "id",
            "oauth2_client_secret": "secret",
            "oauth2_enable_pkce": "1",
            "oauth2_pkce_code_challenge_method": "S256",
            "oauth2_scopes": "some scope",
            "oauth2_login_url": "https://example.com/login/",
            "oauth2_token_url": "https://example.com/token/",
            "oauth2_token_extra_headers": "",
            "oauth2_json_token_path": "access_token",
            "oauth2_user_url": "https://example.com/user/",
            "oauth2_user_method": "GET",
            "oauth2_user_token_location": "HEADER",
            "oauth2_user_token_name": "access_token",
            "oauth2_user_extra_headers": "",
            "oauth2_send_welcome_email": "",
            "oauth2_json_id_path": "id",
            "oauth2_json_name_path": "name",
            "oauth2_json_email_path": "email",
            "oauth2_json_avatar_path": "avatar",
        },
    )

    assert response.status_code == 302

    settings = {row.setting: row.value for row in Setting.objects.all()}

    assert settings["enable_oauth2_client"] is True
    assert settings["oauth2_provider"] == "Lorem"
    assert settings["oauth2_client_id"] == "id"
    assert settings["oauth2_client_secret"] == "secret"
    assert settings["oauth2_enable_pkce"] is True
    assert settings["oauth2_pkce_code_challenge_method"] == "S256"
    assert settings["oauth2_scopes"] == "some scope"
    assert settings["oauth2_login_url"] == "https://example.com/login/"
    assert settings["oauth2_token_url"] == "https://example.com/token/"
    assert settings["oauth2_token_extra_headers"] == ""
    assert settings["oauth2_json_token_path"] == "access_token"
    assert settings["oauth2_user_url"] == "https://example.com/user/"
    assert settings["oauth2_user_method"] == "GET"
    assert settings["oauth2_user_token_location"] == "HEADER"
    assert settings["oauth2_user_token_name"] == "access_token"
    assert settings["oauth2_user_extra_headers"] == ""
    assert settings["oauth2_send_welcome_email"] is False
    assert settings["oauth2_json_id_path"] == "id"
    assert settings["oauth2_json_name_path"] == "name"
    assert settings["oauth2_json_email_path"] == "email"
    assert settings["oauth2_json_avatar_path"] == "avatar"
