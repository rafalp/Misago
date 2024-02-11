from base64 import urlsafe_b64encode
from hashlib import sha256
from secrets import token_urlsafe
from typing import Any
from urllib.parse import urlencode

import requests
from django.urls import reverse
from django.utils.crypto import get_random_string
from requests.exceptions import RequestException

from . import exceptions

SESSION_STATE = "oauth2_state"
STATE_LENGTH = 40
REQUESTS_TIMEOUT = 30
SESSION_CODE_VERIFIER = "oauth2_code_verifier"


def create_login_url(request):
    state = get_random_string(STATE_LENGTH)
    request.session[SESSION_STATE] = state

    querystring = {
        "response_type": "code",
        "client_id": request.settings.oauth2_client_id,
        "redirect_uri": get_redirect_uri(request),
        "scope": request.settings.oauth2_scopes,
        "state": state,
    }

    if request.settings.oauth2_enable_pkce:
        code_verifier = token_urlsafe()
        request.session[SESSION_CODE_VERIFIER] = code_verifier
        querystring["code_challenge"] = get_code_challenge(
            code_verifier, request.settings.oauth2_pkce_code_challenge_method
        )
        querystring["code_challenge_method"] = (
            request.settings.oauth2_pkce_code_challenge_method
        )

    return "%s?%s" % (request.settings.oauth2_login_url, urlencode(querystring))


def get_code_grant(request):
    session_state = request.session.pop(SESSION_STATE, None)

    if request.GET.get("error") == "access_denied":
        raise exceptions.OAuth2AccessDeniedError()

    if not session_state:
        raise exceptions.OAuth2StateNotSetError()

    provider_state = request.GET.get("state")
    if not provider_state:
        raise exceptions.OAuth2StateNotProvidedError()
    if provider_state != session_state:
        raise exceptions.OAuth2StateMismatchError()

    code_grant = request.GET.get("code")
    if not code_grant:
        raise exceptions.OAuth2CodeNotProvidedError()

    return code_grant


def get_access_token(request, code_grant):
    token_url = request.settings.oauth2_token_url
    data = {
        "grant_type": "authorization_code",
        "client_id": request.settings.oauth2_client_id,
        "client_secret": request.settings.oauth2_client_secret,
        "redirect_uri": get_redirect_uri(request),
        "code": code_grant,
    }
    if request.settings.oauth2_enable_pkce:
        data["code_verifier"] = request.session.pop(SESSION_CODE_VERIFIER, None)

    headers = get_headers_dict(request.settings.oauth2_token_extra_headers)

    try:
        r = requests.post(
            token_url,
            data=data,
            headers=headers,
            timeout=REQUESTS_TIMEOUT,
        )
    except RequestException:
        raise exceptions.OAuth2AccessTokenRequestError()

    if r.status_code != 200:
        raise exceptions.OAuth2AccessTokenResponseError()

    try:
        response_json = r.json()
        if not isinstance(response_json, dict):
            raise TypeError()
    except (ValueError, TypeError):
        raise exceptions.OAuth2AccessTokenJSONError()

    access_token = get_value_from_json(
        request.settings.oauth2_json_token_path,
        response_json,
    )

    if not access_token:
        raise exceptions.OAuth2AccessTokenNotProvidedError()

    return access_token


JSON_MAPPING = {
    "id": "oauth2_json_id_path",
    "name": "oauth2_json_name_path",
    "email": "oauth2_json_email_path",
    "avatar": "oauth2_json_avatar_path",
}


def get_user_data(request, access_token):
    headers = get_headers_dict(request.settings.oauth2_user_extra_headers)
    user_url = request.settings.oauth2_user_url

    if request.settings.oauth2_user_token_location == "QUERY":
        user_url += "&" if "?" in user_url else "?"
        user_url += urlencode({request.settings.oauth2_user_token_name: access_token})
    elif request.settings.oauth2_user_token_location == "HEADER_BEARER":
        headers[request.settings.oauth2_user_token_name] = f"Bearer {access_token}"
    else:
        headers[request.settings.oauth2_user_token_name] = access_token

    try:
        if request.settings.oauth2_user_method == "GET":
            r = requests.get(user_url, headers=headers, timeout=REQUESTS_TIMEOUT)
        else:
            r = requests.post(user_url, headers=headers, timeout=REQUESTS_TIMEOUT)
    except RequestException:
        raise exceptions.OAuth2UserDataRequestError()

    if r.status_code != 200:
        raise exceptions.OAuth2UserDataResponseError()

    try:
        response_json = r.json()
        if not isinstance(response_json, dict):
            raise TypeError()
    except (ValueError, TypeError):
        raise exceptions.OAuth2UserDataJSONError()

    user_data = {
        key: get_value_from_json(getattr(request.settings, setting), response_json)
        for key, setting in JSON_MAPPING.items()
    }

    return user_data, response_json


def get_redirect_uri(request):
    return request.build_absolute_uri(reverse("misago:oauth2-complete"))


def get_headers_dict(headers_str):
    headers = {}
    if not headers_str:
        return headers

    for header in headers_str.splitlines():
        header = header.strip()
        if ":" not in header:
            continue

        header_name, header_value = [part.strip() for part in header.split(":", 1)]
        if header_name and header_value:
            headers[header_name] = header_value

    return headers


def get_value_from_json(path, json):
    if not path:
        return None

    if "." not in path:
        return clear_json_value(json.get(path))

    data = json
    for path_part in path.split("."):
        if not isinstance(data, dict):
            return None

        data = data.get(path_part)
        if data is None:
            return None

    return clear_json_value(data)


def clear_json_value(value: Any) -> str | None:
    if isinstance(value, str):
        return value.strip() or None

    if isinstance(value, int) and value is not True and value is not False:
        return str(value)

    return None


def get_code_challenge(code_verifier: str, code_challenge_method: str) -> str:
    if not code_verifier:
        raise exceptions.OAuth2CodeVerifierNotProvidedError()

    if code_challenge_method == "plain":
        return code_verifier
    elif code_challenge_method == "S256":
        return (
            urlsafe_b64encode(sha256(code_verifier.encode("ascii")).digest())
            .decode("ascii")
            .rstrip("=")
        )

    raise exceptions.OAuth2NotSupportedHashMethodError()
