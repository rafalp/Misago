from unittest.mock import Mock

import pytest

from ...users import signatures


@pytest.fixture
def signature(user):
    user.signature = "Test"
    user.signature_parsed = "Test"
    user.signature_checksum = "Test"
    user.save()


def test_user_signature_and_valid_checksum_is_set(user, signature, user_acl):
    request = Mock(scheme="http", get_host=Mock(return_value="127.0.0.1:800"))
    signatures.set_user_signature(request, user, user_acl, "Changed")

    assert user.signature == "Changed"
    assert user.signature_parsed == "<p>Changed</p>"
    assert user.signature_checksum
    assert signatures.is_user_signature_valid(user)


def test_user_signature_is_cleared(user, signature, user_acl):
    request = Mock(scheme="http", get_host=Mock(return_value="127.0.0.1:800"))
    signatures.set_user_signature(request, user, user_acl, "")

    assert not user.signature
    assert not user.signature_parsed
    assert not user.signature_checksum


def test_signature_validity_check_fails_for_incorrect_signature_checksum(
    user, signature
):
    assert not signatures.is_user_signature_valid(user)
