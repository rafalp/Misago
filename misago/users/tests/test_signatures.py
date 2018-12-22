from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.acl.useracl import get_user_acl
from misago.conftest import get_cache_versions
from misago.users import signatures

User = get_user_model()
cache_versions = get_cache_versions()


class MockRequest(object):
    scheme = "http"

    def get_host(self):
        return "127.0.0.1:8000"


class UserSignatureTests(TestCase):
    def test_user_signature_and_valid_checksum_is_set(self):
        user = User.objects.create_user("Bob", "bob@bob.com")
        user.signature = "Test"
        user.signature_parsed = "Test"
        user.signature_checksum = "Test"
        user.save()

        request = Mock(scheme="http", get_host=Mock(return_value="127.0.0.1:800"))
        user_acl = get_user_acl(user, cache_versions)

        signatures.set_user_signature(request, user, user_acl, "Changed")

        assert user.signature == "Changed"
        assert user.signature_parsed == "<p>Changed</p>"
        assert user.signature_checksum
        assert signatures.is_user_signature_valid(user)

    def test_user_signature_is_cleared(self):
        user = User.objects.create_user("Bob", "bob@bob.com")
        user.signature = "Test"
        user.signature_parsed = "Test"
        user.signature_checksum = "Test"
        user.save()

        request = Mock(scheme="http", get_host=Mock(return_value="127.0.0.1:800"))
        user_acl = get_user_acl(user, cache_versions)

        signatures.set_user_signature(request, user, user_acl, "")

        assert not user.signature
        assert not user.signature_parsed
        assert not user.signature_checksum

    def test_signature_validity_check_fails_for_incorrect_signature_checksum(self):
        user = User.objects.create_user("Bob", "bob@bob.com")
        user.signature = "Test"
        user.signature_parsed = "Test"
        user.signature_checksum = "Test"
        user.save()

        assert not signatures.is_user_signature_valid(user)
