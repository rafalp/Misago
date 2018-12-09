from unittest.mock import Mock

from django.contrib.auth import get_user_model

from misago.users.online.utils import get_user_status
from misago.users.testutils import AuthenticatedUserTestCase

User = get_user_model()


class GetUserStatusTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.other_user = User.objects.create_user('Tyrael', 't123@test.com', 'pass123')

    def test_user_hiding_presence(self):
        """get_user_status has no showstopper for hidden user"""
        self.other_user.is_hiding_presence = True
        self.other_user.save()

        request = Mock(
            user=self.user,
            user_acl={'can_see_hidden_users': False},
            cache_versions={"bans": "abcdefgh"},
        )
        get_user_status(request, self.other_user)

    def test_user_visible_hidden_presence(self):
        """get_user_status has no showstopper forvisible  hidden user"""
        self.other_user.is_hiding_presence = True
        self.other_user.save()

        request = Mock(
            user=self.user,
            user_acl={'can_see_hidden_users': True},
            cache_versions={"bans": "abcdefgh"},
        )
        get_user_status(request, self.other_user)

    def test_user_not_hiding_presence(self):
        """get_user_status has no showstoppers for non-hidden user"""
        request = Mock(
            user=self.user,
            user_acl={'can_see_hidden_users': False},
            cache_versions={"bans": "abcdefgh"},
        )
        get_user_status(request, self.other_user)
