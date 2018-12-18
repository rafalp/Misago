from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.acl.useracl import get_user_acl
from misago.users.models import AnonymousUser

User = get_user_model()

cache_versions = {"acl": "abcdefgh"}


class GettingUserACLTests(TestCase):
    def test_getter_returns_authenticated_user_acl(self):
        user = User.objects.create_user('Bob', 'bob@bob.com')
        acl = get_user_acl(user, cache_versions)

        assert acl
        assert acl["user_id"] == user.id
        assert acl["is_authenticated"] is True
        assert acl["is_anonymous"] is False

    def test_user_acl_includes_staff_and_superuser_false_status(self):
        user = User.objects.create_user('Bob', 'bob@bob.com')
        acl = get_user_acl(user, cache_versions)

        assert acl
        assert acl["is_staff"] is False
        assert acl["is_superuser"] is False

    def test_user_acl_includes_cache_versions(self):
        user = User.objects.create_user('Bob', 'bob@bob.com')
        acl = get_user_acl(user, cache_versions)

        assert acl
        assert acl["cache_versions"] == cache_versions

    def test_getter_returns_anonymous_user_acl(self):
        user = AnonymousUser()
        acl = get_user_acl(user, cache_versions)

        assert acl
        assert acl["user_id"] == user.id
        assert acl["is_authenticated"] is False
        assert acl["is_anonymous"] is True

    def test_superuser_acl_includes_staff_and_superuser_true_status(self):
        user = User.objects.create_superuser('Bob', 'bob@bob.com', 'Pass.123')
        acl = get_user_acl(user, cache_versions)

        assert acl
        assert acl["is_staff"] is True
        assert acl["is_superuser"] is True

    @patch('django.core.cache.cache.get', return_value=dict())
    def test_getter_returns_acl_from_cache(self, cache_get):
        user = AnonymousUser()
        get_user_acl(user, cache_versions)
        cache_get.assert_called_once()

    @patch('django.core.cache.cache.set')
    @patch('misago.acl.buildacl.build_acl', return_value=dict())
    @patch('django.core.cache.cache.get', return_value=None)
    def test_getter_builds_new_acl_when_cache_is_not_available(self, cache_get, *_):
        user = AnonymousUser()
        get_user_acl(user, cache_versions)
        cache_get.assert_called_once()

    @patch('django.core.cache.cache.set')
    @patch('misago.acl.buildacl.build_acl', return_value=dict())
    @patch('django.core.cache.cache.get', return_value=None)
    def test_getter_sets_new_cache_if_no_cache_is_set(self, cache_set, *_):
        user = AnonymousUser()
        get_user_acl(user, cache_versions)
        cache_set.assert_called_once()


    @patch('django.core.cache.cache.set')
    @patch('misago.acl.buildacl.build_acl', return_value=dict())
    @patch('django.core.cache.cache.get', return_value=None)
    def test_acl_cache_name_includes_cache_verssion(self, cache_set, *_):
        user = AnonymousUser()
        get_user_acl(user, cache_versions)
        cache_key = cache_set.call_args[0][0]
        assert cache_versions["acl"] in cache_key

    @patch('django.core.cache.cache.set')
    @patch('django.core.cache.cache.get', return_value=dict())
    def test_getter_is_not_setting_new_cache_if_cache_is_set(self, _, cache_set):
        user = AnonymousUser()
        get_user_acl(user, cache_versions)
        cache_set.assert_not_called()