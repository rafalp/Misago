from unittest.mock import Mock

from django.contrib.auth import get_user_model

from misago.acl.testutils import override_acl
from misago.users.online.utils import get_user_status
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class GetUserStatusTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.other_user = UserModel.objects.create_user('Tyrael', 't123@test.com', 'pass123')

    def test_user_hiding_presence(self):
        """get_user_status has no showstopper for hidden user"""
        self.other_user.is_hiding_presence = True
        self.other_user.save()

        request = Mock(user=self.user, cache_versions={"bans": "abcdfghi"})
        get_user_status(request, self.other_user)

    def test_user_visible_hidden_presence(self):
        """get_user_status has no showstopper forvisible  hidden user"""
        self.other_user.is_hiding_presence = True
        self.other_user.save()

        override_acl(self.user, {
            'can_see_hidden_users': True,
        })

        request = Mock(user=self.user, cache_versions={"bans": "abcdfghi"})
        get_user_status(request, self.other_user)

    def test_user_not_hiding_presence(self):
        """get_user_status has no showstoppers for non-hidden user"""
        request = Mock(user=self.user, cache_versions={"bans": "abcdfghi"})
        get_user_status(request, self.other_user)
