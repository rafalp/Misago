from urllib.parse import urlencode

import requests
from django.urls import reverse
from django.utils.crypto import get_random_string

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


def receive_code(request):
    state = request.session.pop(SESSION_STATE, None)
    if not state:
        raise ValueError("'state' is missing from Misago session")

    redirect_state = request.GET.get("state")
    if not redirect_state:
        raise ValueError("'state' is missing from redirect URL")
    if redirect_state != state:
        raise ValueError("'state' is different from one in session")

    redirect_code = request.GET.get("code")
    if not redirect_code:
        raise ValueError("'code' is missing from redirect URL")

    return redirect_code


def exchange_code_for_token(request, code):
    token_url = request.settings.oauth2_token_url
    data = {
        "grant_type": "authorization_code",
        "client_id": request.settings.oauth2_client_id,
        "client_secret": request.settings.oauth2_client_secret,
        "redirect_uri": get_redirect_uri(request),
        "code": code,
    }

    if request.settings.oauth2_token_method == "GET":
        token_url += "&" if "?" in token_url else "?"
        token_url += urlencode(data)
        r = requests.get(token_url, timeout=REQUESTS_TIMEOUT)
    else:
        r = request.post(token_url, data=data, timeout=REQUESTS_TIMEOUT)

    if r.status_code != 200:
        raise ValueError(
            f"Failed to exchange code for token: '{r.content}' ({r.status_code})"
        )

    try:
        response_json = r.json()
    except (ValueError, TypeError):
        raise ValueError(f"Could not parse response as JSON: '{r.content}'")

    access_token = get_value_from_json(
        request.settings.oauth2_json_token_path,
        response_json,
    )

    if not access_token:
        raise ValueError(f"Could not find access token in the response: '{r.content}'")

    return access_token


JSON_MAPPING = {
    "id": "oauth2_json_id_path",
    "name": "oauth2_json_name_path",
    "email": "oauth2_json_email_path",
    "avatar": "oauth2_json_avatar_path",
}


def retrieve_user_data(request, access_token):
    headers = None
    user_url = request.settings.oauth2_user_url

    if request.settings.oauth2_user_token_location == "QUERY":
        user_url += "&" if "?" in user_url else "?"
        user_url += urlencode({request.settings.oauth2_user_token_name: access_token})
    elif request.settings.oauth2_user_token_location == "HEADER_BEARER":
        headers = {request.settings.oauth2_user_token_name: f"Bearer {access_token}"}
    else:
        headers = {request.settings.oauth2_user_token_name: access_token}

    if request.settings.oauth2_user_method == "GET":
        r = requests.get(user_url, headers=headers, timeout=REQUESTS_TIMEOUT)
    else:
        r = requests.post(user_url, headers=headers, timeout=REQUESTS_TIMEOUT)

    if r.status_code != 200:
        raise ValueError(
            f"Failed to retrieve user data: '{r.content}' ({r.status_code})"
        )

    try:
        response_json = r.json()
    except (ValueError, TypeError):
        raise ValueError(f"Could not parse response as JSON: '{r.content}'")

    return {
        key: get_value_from_json(getattr(request.settings, setting), response_json)
        for key, setting in JSON_MAPPING.items()
    }


def get_redirect_uri(request):
    return request.build_absolute_uri(reverse("misago:oauth2-complete"))


def get_value_from_json(path, json):
    if not path:
        return None

    if "." not in path:
        return json.get(path)

    data = json
    for path_part in path.split("."):
        data = data.get(path_part)
        if not data:
            return None

    return data
