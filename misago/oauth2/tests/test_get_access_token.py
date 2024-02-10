from unittest.mock import Mock, patch

import pytest
from requests.exceptions import Timeout

from ...conf.test import override_dynamic_settings
from .. import exceptions
from ..client import (
    REQUESTS_TIMEOUT,
    SESSION_CODE_VERIFIER,
    get_access_token,
)

ACCESS_TOKEN = "acc3ss-t0k3n"
CODE_GRANT = "valid-code"


@pytest.fixture
def mock_request(dynamic_settings):
    return Mock(
        settings=dynamic_settings,
        build_absolute_uri=lambda url: f"http://mysite.com{url or ''}",
    )


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
)
def test_access_token_is_retrieved_using_post_request(mock_request):
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
        assert get_access_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        post_mock.assert_called_once_with(
            "https://example.com/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "clientid123",
                "client_secret": "secr3t",
                "redirect_uri": "http://mysite.com/oauth2/complete/",
                "code": CODE_GRANT,
            },
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_token_extra_headers="Accept: application/json\nApi-Ver:1234",
)
def test_access_token_is_retrieved_using_extra_headers(mock_request):
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
        assert get_access_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        post_mock.assert_called_once_with(
            "https://example.com/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "clientid123",
                "client_secret": "secr3t",
                "redirect_uri": "http://mysite.com/oauth2/complete/",
                "code": CODE_GRANT,
            },
            headers={
                "Accept": "application/json",
                "Api-Ver": "1234",
            },
            timeout=REQUESTS_TIMEOUT,
        )


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
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
        assert get_access_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
)
def test_exception_is_raised_if_access_token_request_times_out(mock_request):
    post_mock = Mock(side_effect=Timeout())

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2AccessTokenRequestError):
            get_access_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
)
def test_exception_is_raised_if_access_token_request_response_is_not_200(mock_request):
    post_mock = Mock(
        return_value=Mock(
            status_code=400,
        ),
    )

    with patch("requests.post", post_mock):
        with pytest.raises(exceptions.OAuth2AccessTokenResponseError):
            get_access_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
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
            get_access_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
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
            get_access_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
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
            get_access_token(mock_request, CODE_GRANT)

        post_mock.assert_called_once()


@override_dynamic_settings(
    oauth2_client_id="clientid123",
    oauth2_client_secret="secr3t",
    oauth2_token_url="https://example.com/oauth2/token",
    oauth2_enable_pkce=True,
)
def test_access_token_is_retrieved_using_post_request_with_pkce_enabled(mock_request):
    code_verifier = "KUnVU1"
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
    mock_request.session = {SESSION_CODE_VERIFIER: code_verifier}

    with patch("requests.post", post_mock):
        assert get_access_token(mock_request, CODE_GRANT) == ACCESS_TOKEN

        post_mock.assert_called_once_with(
            "https://example.com/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "clientid123",
                "client_secret": "secr3t",
                "redirect_uri": "http://mysite.com/oauth2/complete/",
                "code": CODE_GRANT,
                "code_verifier": code_verifier,
            },
            headers={},
            timeout=REQUESTS_TIMEOUT,
        )
        # code verifier was removed from session
        assert SESSION_CODE_VERIFIER not in mock_request.session
