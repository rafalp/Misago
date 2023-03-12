from urllib.parse import urlencode

import requests
from django.urls import reverse
from django.utils.crypto import get_random_string
from requests.exceptions import RequestException

from . import exceptions

SESSION_STATE = "oauth2_state"
STATE_LENGTH = 40
REQUESTS_TIMEOUT = 30


def create_login_url(request):
    state = get_random_string(STATE_LENGTH)
    request.session[SESSION_STATE] = state

    quote = {
        "response_type": "code",
        "client_id": request.settings.oauth2_client_id,
        "redirect_uri": get_redirect_uri(request),
        "scope": request.settings.oauth2_scopes,
        "state": state,
    }

    return "%s?%s" % (request.settings.oauth2_login_url, urlencode(quote))


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

    clean_data = {
        key: get_value_from_json(getattr(request.settings, setting), response_json)
        for key, setting in JSON_MAPPING.items()
    }

    return clean_data, response_json


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
        return str(json.get(path, "")).strip() or None

    data = json
    for path_part in path.split("."):
        data = data.get(path_part)
        if not data:
            return None

    return data
