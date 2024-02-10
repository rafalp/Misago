import pytest

from .. import exceptions
from ..client import get_code_challenge


def test_exception_is_raised_if_code_verifier_is_not_provided():
    with pytest.raises(exceptions.OAuth2CodeVerifierNotProvidedError):
        get_code_challenge(None, "S256")

    with pytest.raises(exceptions.OAuth2CodeVerifierNotProvidedError):
        get_code_challenge("", "S256")


def test_exception_is_raised_if_code_challenge_method_is_not_supported():
    with pytest.raises(exceptions.OAuth2NotSupportedHashMethodError):
        get_code_challenge("hYfgN", "ABC")


def test_code_challenge_is_returned_using_S256_hash_method():
    code_verifier = "hYfgNABC"
    code_challenge = "E5AZUNDQx0-aVDeEVgNFTEglcG1bWgOuygG_elkz_io"
    assert get_code_challenge(code_verifier, "S256") == code_challenge


def test_code_challenge_is_returned_using_plain_hash_method():
    code_verifier = "hYfgNABC"
    assert get_code_challenge(code_verifier, "plain") == code_verifier
