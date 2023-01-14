from unittest.mock import Mock

import pytest

from .. import exceptions
from ..client import SESSION_STATE, get_code_grant


def test_code_grant_is_returned_from_request():
    state = "l0r3m1p5um"
    code_grant = "valid-code"

    request = Mock(
        GET={
            "state": state,
            "code": code_grant,
        },
        session={SESSION_STATE: state},
    )

    assert get_code_grant(request) == code_grant

    # State was removed from session
    assert SESSION_STATE not in request.session


def test_exception_is_raised_if_provider_returned_error():
    request = Mock(
        GET={"error": "access_denied"},
        session={},
    )

    with pytest.raises(exceptions.OAuth2AccessDeniedError):
        get_code_grant(request)

    # State was removed from session
    assert SESSION_STATE not in request.session


def test_exception_is_raised_if_session_is_missing_state():
    state = "l0r3m1p5um"
    code_grant = "valid-code"

    request = Mock(
        GET={
            "state": state,
            "code": code_grant,
        },
        session={},
    )

    with pytest.raises(exceptions.OAuth2StateNotSetError):
        get_code_grant(request)


def test_exception_is_raised_if_request_is_missing_state():
    state = "l0r3m1p5um"
    code_grant = "valid-code"

    request = Mock(
        GET={
            "code": code_grant,
        },
        session={SESSION_STATE: state},
    )

    with pytest.raises(exceptions.OAuth2StateNotProvidedError):
        get_code_grant(request)

    # State was removed from session
    assert SESSION_STATE not in request.session


def test_exception_is_raised_if_request_state_is_empty():
    state = "l0r3m1p5um"
    code_grant = "valid-code"

    request = Mock(
        GET={
            "state": "",
            "code": code_grant,
        },
        session={SESSION_STATE: state},
    )

    with pytest.raises(exceptions.OAuth2StateNotProvidedError):
        get_code_grant(request)

    # State was removed from session
    assert SESSION_STATE not in request.session


def test_exception_is_raised_if_session_state_doesnt_match_with_request():
    state = "l0r3m1p5um"
    code_grant = "valid-code"

    request = Mock(
        GET={
            "state": "invalid",
            "code": code_grant,
        },
        session={SESSION_STATE: state},
    )

    with pytest.raises(exceptions.OAuth2StateMismatchError):
        get_code_grant(request)

    # State was removed from session
    assert SESSION_STATE not in request.session


def test_exception_is_raised_if_request_is_missing_code_grant():
    state = "l0r3m1p5um"

    request = Mock(
        GET={
            "state": state,
        },
        session={SESSION_STATE: state},
    )

    with pytest.raises(exceptions.OAuth2CodeNotProvidedError):
        get_code_grant(request)

    # State was removed from session
    assert SESSION_STATE not in request.session


def test_exception_is_raised_if_request_code_grant_is_empty():
    state = "l0r3m1p5um"

    request = Mock(
        GET={
            "code": "",
            "state": state,
        },
        session={SESSION_STATE: state},
    )

    with pytest.raises(exceptions.OAuth2CodeNotProvidedError):
        get_code_grant(request)

    # State was removed from session
    assert SESSION_STATE not in request.session
