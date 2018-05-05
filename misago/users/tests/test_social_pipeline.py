from django.contrib.auth import get_user_model
from social_core.backends.github import GithubOAuth2

from misago.core.exceptions import SocialAuthFailed, SocialAuthBanned

from misago.users.models import Ban
from misago.users.social.pipeline import (
    associate_by_email, validate_ip_not_banned, validate_user_not_banned
)
from misago.users.testutils import UserTestCase


UserModel = get_user_model()


class MockRequest(object):
    def __init__(self, user_ip='0.0.0.0'):
        self.session = {}
        self.user_ip = user_ip


class MockStrategy(object):
    def __init__(self, user_ip='0.0.0.0'):
        self.request = MockRequest(user_ip=user_ip)


class PipelineTestCase(UserTestCase):
    def get_initial_user(self):
        self.user = self.get_authenticated_user()


class AssociateByEmailTests(PipelineTestCase):
    def test_skip_if_user_is_already_set(self):
        """pipeline step is skipped if user was found by previous step"""
        result = associate_by_email(None, {}, GithubOAuth2, self.user)
        self.assertIsNone(result)

    def test_skip_if_no_email_passed(self):
        """pipeline step is skipped if no email was passed"""
        result = associate_by_email(None, {}, GithubOAuth2)
        self.assertIsNone(result)

    def test_skip_if_user_with_email_not_found(self):
        """pipeline step is skipped if no email was passed"""
        result = associate_by_email(None, {'email': 'not@found.com'}, GithubOAuth2)
        self.assertIsNone(result)

    def test_raise_if_user_is_inactive(self):
        """pipeline raises if user was inactive"""
        self.user.is_active = False
        self.user.save()

        try:
            associate_by_email(None, {'email': self.user.email}, GithubOAuth2)
            self.fail("associate_by_email should raise SocialAuthFailed")
        except SocialAuthFailed as e:
            self.assertEqual(
                e.message,
                (
                    "The e-mail address associated with your GitHub account is not available for "
                    "use on this site."
                ),
            )

    def test_raise_if_user_needs_admin_activation(self):
        """pipeline raises if user needs admin activation"""
        self.user.requires_activation = UserModel.ACTIVATION_ADMIN
        self.user.save()

        try:
            associate_by_email(None, {'email': self.user.email}, GithubOAuth2)
            self.fail("associate_by_email should raise SocialAuthFailed")
        except SocialAuthFailed as e:
            self.assertEqual(
                e.message,
                (
                    "Your account has to be activated by site administrator before you will be "
                    "able to sign in with GitHub."
                ),
            )

    def test_return_user(self):
        """pipeline returns user if email was found"""
        result = associate_by_email(None, {'email': self.user.email}, GithubOAuth2)
        self.assertEqual(result, {'user': self.user, 'is_new': False})
    
    def test_return_user_email_inactive(self):
        """pipeline returns user even if they didn't activate their account manually"""
        self.user.requires_activation = UserModel.ACTIVATION_USER
        self.user.save()

        result = associate_by_email(None, {'email': self.user.email}, GithubOAuth2)
        self.assertEqual(result, {'user': self.user, 'is_new': False})
    

class ValidateIpNotBannedTests(PipelineTestCase):
    def test_skip_if_user_not_set(self):
        """pipeline step is skipped if no user was passed"""
        result = associate_by_email(None, {}, GithubOAuth2)
        self.assertIsNone(result)

    def test_raise_if_banned(self):
        """pipeline raises if user's IP is banned"""
        Ban.objects.create(banned_value='188.*', check_type=Ban.IP)

        try:
            validate_ip_not_banned(MockStrategy(user_ip='188.1.2.3'), {}, GithubOAuth2, self.user)
            self.fail("validate_ip_not_banned should raise SocialAuthBanned")
        except SocialAuthBanned as e:
            self.assertEqual(e.ban, {
                'version': 0,
                'ip': '188.1.2.3',
                'expires_on': None,
                'is_banned': True,
                'message': None,
            })

    def test_exclude_staff(self):
        """pipeline excludes staff from bans"""
        self.user.is_staff = True
        self.user.save()

        Ban.objects.create(banned_value='188.*', check_type=Ban.IP)

        result = validate_ip_not_banned(MockStrategy(user_ip='188.1.2.3'), {}, GithubOAuth2, self.user)
        self.assertIsNone(result)


class ValidateUserNotBannedTests(PipelineTestCase):
    def test_skip_if_user_not_set(self):
        """pipeline step is skipped if no user was passed"""
        result = associate_by_email(None, {}, GithubOAuth2)
        self.assertIsNone(result)

    def test_raise_if_banned(self):
        """pipeline raises if user's IP is banned"""
        Ban.objects.create(banned_value=self.user.username, check_type=Ban.USERNAME)

        try:
            validate_user_not_banned(MockStrategy(), {}, GithubOAuth2, self.user)
            self.fail("validate_ip_not_banned should raise SocialAuthBanned")
        except SocialAuthBanned as e:
            self.assertEqual(e.ban.user, self.user)

    def test_exclude_staff(self):
        """pipeline excludes staff from bans"""
        self.user.is_staff = True
        self.user.save()

        Ban.objects.create(banned_value=self.user.username, check_type=Ban.USERNAME)

        result = validate_user_not_banned(MockStrategy(), {}, GithubOAuth2, self.user)
        self.assertIsNone(result)
