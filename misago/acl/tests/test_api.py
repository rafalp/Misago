from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.acl.api import get_user_acl
from misago.users.models import AnonymousUser


UserModel = get_user_model()


class GetUserACLTests(TestCase):
    def test_get_authenticated_acl(self):
        """get ACL for authenticated user"""
        test_user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        acl = get_user_acl(test_user)

        self.assertTrue(acl)
        self.assertEqual(acl, test_user.acl_cache)

    def test_get_anonymous_acl(self):
        """get ACL for unauthenticated user"""
        acl = get_user_acl(AnonymousUser())

        self.assertTrue(acl)
        self.assertEqual(acl, AnonymousUser().acl_cache)
