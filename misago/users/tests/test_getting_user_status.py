from unittest.mock import Mock

from ..online.utils import get_user_status
from ..test import AuthenticatedUserTestCase, create_test_user


class GetUserStatusTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.other_user = create_test_user("OtherUser", "otheruser@example.com")

    def test_get_visible_user_status_returns_online(self):
        request = Mock(
            user=self.user,
            user_acl={"can_see_hidden_users": False},
            cache_versions={"bans": "abcdefgh"},
        )
        assert get_user_status(request, self.other_user)["is_online"]

    def test_get_hidden_user_status_without_seeing_hidden_permission_returns_offline(
        self
    ):
        """get_user_status has no showstopper for hidden user"""
        self.other_user.is_hiding_presence = True
        self.other_user.save()

        request = Mock(
            user=self.user,
            user_acl={"can_see_hidden_users": False},
            cache_versions={"bans": "abcdefgh"},
        )
        assert get_user_status(request, self.other_user)["is_hidden"]

    def test_get_hidden_user_status_with_seeing_hidden_permission_returns_online_hidden(
        self
    ):
        self.other_user.is_hiding_presence = True
        self.other_user.save()

        request = Mock(
            user=self.user,
            user_acl={"can_see_hidden_users": True},
            cache_versions={"bans": "abcdefgh"},
        )
        assert get_user_status(request, self.other_user)["is_online_hidden"]
