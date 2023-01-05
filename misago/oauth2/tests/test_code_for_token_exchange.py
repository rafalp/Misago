from unittest.mock import Mock, patch

import pytest
from requests.exceptions import Timeout

from ...conf.test import override_dynamic_settings
from .. import exceptions
from ..client import REQUESTS_TIMEOUT, exchange_code_for_token

ACCESS_TOKEN = "acc3ss-t0k3n"
CODE_GRANT = "valid-code"


@pytest.fixture
def mock_request(dynamic_settings):
    return Mock(
        settings=dynamic_settings,
        build_absolute_uri=lambda url: f"http://mysite.com{url or ''}",
    )


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="GET",
)
def test_access_token_is_returned_using_get_request(mock_request):
    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "access_token": ACCESS_TOKEN,
                },
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert exchange_code_for_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        get_mock.assert_called_once_with(
            (
                "https://example.com/oauth2/token"
                "?grant_type=authorization_code"
                "&client_id=clientid123"
                "&client_secret=secr3t"
                "&redirect_uri=http%3A%2F%2Fmysite.com%2Foauth2%2Fcomplete%2F"
                "&code=valid-code"
            ),
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token?exchange=1",
    oauth2_token_method="GET",
)
def test_access_token_exchange_get_request_url_respects_existing_querystring(
    mock_request,
):
    get_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "access_token": ACCESS_TOKEN,
                },
            ),
        ),
    )

    with patch("requests.get", get_mock):
        assert exchange_code_for_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        get_mock.assert_called_once_with(
            (
                "https://example.com/oauth2/token?exchange=1"
                "&grant_type=authorization_code"
                "&client_id=clientid123"
                "&client_secret=secr3t"
                "&redirect_uri=http%3A%2F%2Fmysite.com%2Foauth2%2Fcomplete%2F"
                "&code=valid-code"
            ),
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="POST",
)
def test_access_token_is_returned_using_post_request(mock_request):
    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "access_token": ACCESS_TOKEN,
                },
            ),
        ),
    )

    with patch("requests.post", post_mock):
        assert exchange_code_for_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        post_mock.assert_called_once_with(
            "https://example.com/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "clientid123",
                "client_secret": "secr3t",
                "redirect_uri": "http://mysite.com/oauth2/complete/",
                "code": CODE_GRANT,
            },
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="POST",
    oauth2_json_token_path="data.auth.token",
)
def test_access_token_is_extracted_from_json(mock_request):
    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "data": {
                        "auth": {
                            "token": ACCESS_TOKEN,
                        },
                    },
                },
            ),
        ),
    )

    with patch("requests.post", post_mock):
        assert exchange_code_for_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        post_mock.assert_called_once()


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="POST",
)
def test_exception_is_raised_if_access_token_request_times_out(mock_request):
    post_mock = Mock(side_effect=Timeout())

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2AccessTokenRequestError):
            exchange_code_for_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="POST",
)
def test_exception_is_raised_if_access_token_request_response_is_not_200(mock_request):
    post_mock = Mock(
        return_value=Mock(
            status_code=400,
        ),
    )

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2AccessTokenResponseError):
            exchange_code_for_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="POST",
)
def test_exception_is_raised_if_access_token_request_response_is_not_json(mock_request):
    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                side_effect=ValueError(),
            ),
        ),
    )

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2AccessTokenJSONError):
            exchange_code_for_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="POST",
)
def test_exception_is_raised_if_access_token_request_response_json_is_not_object(
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
        with pytest.raises(exceptions.OAuth2AccessTokenJSONError):
            exchange_code_for_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    enable_oauth2_client=True,
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_method="POST",
)
def test_exception_is_raised_if_access_token_request_response_json_misses_token(
    mock_request,
):
    post_mock = Mock(
        return_value=Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "no_token": "nope",
                },
            ),
        ),
    )

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2AccessTokenNotProvidedError):
            exchange_code_for_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()
