from unittest.mock import Mock, patch

import pytest
from requests.exceptions import Timeout

from ...conf.test import override_dynamic_settings
from .. import exceptions
from ..client import REQUESTS_TIMEOUT, get_user_data

ACCESS_TOKEN = "acc3ss-t0k3n"


@pytest.fixture
def mock_request(dynamic_settings):
    return Mock(settings=dynamic_settings)


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/user",
    oauth2_user_method="GET",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_is_returned_using_get_request_with_token_in_query_string(
    mock_request,
):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        get_mock.assert_called_once_with(
            f"https://example.com/oauth2/user?atoken={ACCESS_TOKEN}",
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/user",
    oauth2_user_method="GET",
    oauth2_user_token_name="Authentication",
    oauth2_user_token_location="HEADER",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_is_returned_using_get_request_with_token_in_header(mock_request):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        get_mock.assert_called_once_with(
            f"https://example.com/oauth2/user",
            headers={"Authentication": ACCESS_TOKEN},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/user",
    oauth2_user_method="GET",
    oauth2_user_token_name="Authentication",
    oauth2_user_token_location="HEADER_BEARER",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_is_returned_using_get_request_with_bearer_token_in_header(
    mock_request,
):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        get_mock.assert_called_once_with(
            f"https://example.com/oauth2/user",
            headers={"Authentication": f"Bearer {ACCESS_TOKEN}"},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/user",
    oauth2_user_method="POST",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_is_returned_using_post_request_with_token_in_query_string(
    mock_request,
):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.post", post_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        post_mock.assert_called_once_with(
            f"https://example.com/oauth2/user?atoken={ACCESS_TOKEN}",
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/user",
    oauth2_user_method="POST",
    oauth2_user_token_name="Authentication",
    oauth2_user_token_location="HEADER",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_is_returned_using_post_request_with_token_in_header(mock_request):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.post", post_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        post_mock.assert_called_once_with(
            f"https://example.com/oauth2/user",
            headers={"Authentication": ACCESS_TOKEN},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/user",
    oauth2_user_method="POST",
    oauth2_user_token_name="Authentication",
    oauth2_user_token_location="HEADER_BEARER",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_is_returned_using_post_request_with_bearer_token_in_header(
    mock_request,
):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.post", post_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        post_mock.assert_called_once_with(
            f"https://example.com/oauth2/user",
            headers={"Authentication": f"Bearer {ACCESS_TOKEN}"},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/user",
    oauth2_user_method="POST",
    oauth2_user_token_name="Authentication",
    oauth2_user_token_location="HEADER_BEARER",
    oauth2_user_extra_headers="Accept: application/json\nApi-Ver:1234",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_is_returned_using_post_request_with_extra_headers(
    mock_request,
):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.post", post_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        post_mock.assert_called_once_with(
            f"https://example.com/oauth2/user",
            headers={
                "Authentication": f"Bearer {ACCESS_TOKEN}",
                "Accept": "application/json",
                "Api-Ver": "1234",
            },
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data?type=user",
    oauth2_user_method="GET",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
    oauth2_json_id_path="id",
    oauth2_json_name_path="name",
    oauth2_json_email_path="email",
    oauth2_json_avatar_path="avatar",
)
def test_user_data_request_with_token_in_url_respects_existing_querystring(
    mock_request,
):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=user_data,
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, user_data)

        get_mock.assert_called_once_with(
            f"https://example.com/oauth2/data?type=user&atoken={ACCESS_TOKEN}",
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data?type=user",
    oauth2_user_method="GET",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
    oauth2_json_id_path="id",
    oauth2_json_name_path="user.profile.name",
    oauth2_json_email_path="user.profile.email",
    oauth2_json_avatar_path="user.profile.avatar",
)
def test_user_data_json_values_are_mapped_to_result(mock_request):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    json_response = {
        "id": user_data["id"],
        "user": {
            "profile": {
                "name": user_data["name"],
                "email": user_data["email"],
                "avatar": user_data["avatar"],
            }
        },
    }

    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=json_response,
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, json_response)

        get_mock.assert_called_once_with(
            f"https://example.com/oauth2/data?type=user&atoken={ACCESS_TOKEN}",
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data?type=user",
    oauth2_user_method="GET",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
    oauth2_json_id_path="id",
    oauth2_json_name_path="user.profile.name",
    oauth2_json_email_path="user.profile.email",
    oauth2_json_avatar_path="user.profile.avatar",
)
def test_user_data_json_values_are_none_when_not_found(mock_request):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": "https://example.com/avatar.png",
    }

    json_response = {
        "profile_id": user_data["id"],
        "user": {
            "data": {
                "name": user_data["name"],
                "email": user_data["email"],
                "avatar": user_data["avatar"],
            }
        },
    }

    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=json_response,
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (
            {
                "id": None,
                "name": None,
                "email": None,
                "avatar": None,
            },
            json_response,
        )

        get_mock.assert_called_once_with(
            f"https://example.com/oauth2/data?type=user&atoken={ACCESS_TOKEN}",
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data?type=user",
    oauth2_user_method="GET",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
    oauth2_json_id_path="id",
    oauth2_json_name_path="user.profile.name",
    oauth2_json_email_path="user.profile.email",
    oauth2_json_avatar_path="",
)
def test_user_data_skips_avatar_if_path_is_not_set(mock_request):
    user_data = {
        "id": "7dds8a7dd89sa",
        "name": "Aerith",
        "email": "aerith@example.com",
        "avatar": None,
    }

    json_response = {
        "id": user_data["id"],
        "user": {
            "profile": {
                "name": user_data["name"],
                "email": user_data["email"],
                "avatar": "https://example.com/avatar.png",
            }
        },
    }

    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=json_response,
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert get_user_data(mock_request, ACCESS_TOKEN) == (user_data, json_response)

        get_mock.assert_called_once_with(
            f"https://example.com/oauth2/data?type=user&atoken={ACCESS_TOKEN}",
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data",
    oauth2_user_method="POST",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
)
def test_exception_is_raised_if_user_data_request_times_out(mock_request):
    post_mock = Mock(side_effect=Timeout())

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2UserDataRequestError):
            get_user_data(mock_request, ACCESS_TOKEN)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data",
    oauth2_user_method="POST",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
)
def test_exception_is_raised_if_user_data_request_response_is_not_200(mock_request):
    post_mock = Mock(
        return_value=Mock(
            status_code=400,
        ),
    )

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2UserDataResponseError):
            get_user_data(mock_request, ACCESS_TOKEN)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data",
    oauth2_user_method="POST",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
)
def test_exception_is_raised_if_user_data_request_response_is_not_json(mock_request):
    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                side_effect=ValueError(),
            ),
        ),
    )

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2UserDataJSONError):
            get_user_data(mock_request, ACCESS_TOKEN)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_user_url="https://example.com/oauth2/data",
    oauth2_user_method="POST",
    oauth2_user_token_name="atoken",
    oauth2_user_token_location="QUERY",
)
def test_exception_is_raised_if_user_data_request_response_json_is_not_object(
    mock_request,
):
    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value=["json", "list"],
            ),
        ),
    )

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2UserDataJSONError):
            get_user_data(mock_request, ACCESS_TOKEN)

        post_mock.assert_called_once()
