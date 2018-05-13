# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from social_core.backends.github import GithubOAuth2

from misago.core.exceptions import SocialAuthFailed, SocialAuthBanned

from misago.users.models import AnonymousUser, Ban, BanCache
from misago.users.social.pipeline import (
    associate_by_email, create_user, get_username, validate_ip_not_banned, validate_user_not_banned
)
from misago.users.testutils import UserTestCase


UserModel = get_user_model()


class MockRequest(object):
    def __init__(self, user_ip='0.0.0.0'):
        self.session = {}
        self.user = AnonymousUser()
        self.user_ip = user_ip

    def is_secure(self):
        return False


class MockStrategy(object):
    def __init__(self, request_factory, user_ip='0.0.0.0'):
        factory = RequestFactory()
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
    

class CreateUser(PipelineTestCase):
    def test_skip_if_user_is_set(self):
        """pipeline step is skipped if user was passed"""
        result = create_user(MockStrategy(), {}, GithubOAuth2(), user=self.user)
        self.assertIsNone(result)

    def test_skip_if_no_email_passed(self):
        """pipeline step is skipped if no email was passed"""
        result = create_user(
            MockStrategy(),
            {},
            GithubOAuth2(),
            clean_username='TestBob',
        )
        self.assertIsNone(result)

    def test_skip_if_no_clean_username_passed(self):
        """pipeline step is skipped if cleaned username wasnt passed"""
        result = create_user(
            MockStrategy(),
            {'email': 'hello@example.com'},
            GithubOAuth2(),
        )
        self.assertIsNone(result)

    def test_skip_if_email_is_taken(self):
        """pipeline step is skipped if email was taken"""
        result = create_user(
            MockStrategy(),
            {'email': self.user.email},
            GithubOAuth2(),
            clean_username='NewUser',
        )
        self.assertIsNone(result)

    def test_user_is_created(self):
        """pipeline step returns user if data is correct"""
        result = create_user(
            MockStrategy(),
            {'email': 'new@example.com'},
            GithubOAuth2(),
            clean_username='NewUser',
        )
        new_user = UserModel.objects.get(email='new@example.com')
        self.assertEqual(result, {
            'user': new_user,
            'is_new': True,
        })
        self.assertEqual(new_user.username, 'NewUser')
        self.assertFalse(new_user.has_useable_password())


class GetUsernameTests(PipelineTestCase):
    def test_skip_if_user_is_set(self):
        """pipeline step is skipped if user was passed"""
        result = get_username(None, {}, None, user=self.user)
        self.assertIsNone(result)

    def test_skip_if_no_names(self):
        """pipeline step is skipped if API returned no names"""
        result = get_username(None, {}, None)
        self.assertIsNone(result)

    def test_resolve_to_username(self):
        """pipeline step resolves username"""
        result = get_username(None, {'username': 'BobBoberson'}, None)
        self.assertEqual(result, {'clean_username': 'BobBoberson'})

    def test_normalize_username(self):
        """pipeline step normalizes username"""
        result = get_username(None, {'username': u'Błop Błoperson'}, None)
        self.assertEqual(result, {'clean_username': 'BlopBloperson'})

    def test_resolve_to_first_name(self):
        """pipeline attempts to use first name because username is taken"""
        details = {
            'username': self.user.username,
            'first_name': u'Błob',
        }
        result = get_username(None, details, None)
        self.assertEqual(result, {'clean_username': 'Blob'})

    def test_dont_resolve_to_last_name(self):
        """pipeline will not fallback to last name because username is taken"""
        details = {
            'username': self.user.username,
            'last_name': u'Błob',
        }
        result = get_username(None, details, None)
        self.assertIsNone(result)

    def test_resolve_to_first_last_name_first_char(self):
        """pipeline will construct username from first name and first char of surname"""
        details = {
            'first_name': self.user.username,
            'last_name': u'Błob',
        }
        result = get_username(None, details, None)
        self.assertEqual(result, {'clean_username': self.user.username + 'B'})

    def test_dont_resolve_to_banned_name(self):
        """pipeline will not resolve to banned name"""
        Ban.objects.create(banned_value='*Admin*', check_type=Ban.USERNAME)
        details = {
            'username': 'Misago Admin',
            'first_name': u'Błob',
        }
        result = get_username(None, details, None)
        self.assertEqual(result, {'clean_username': 'Blob'})

    def test_resolve_full_name(self):
        """pipeline will resolve to full name"""
        Ban.objects.create(banned_value='*Admin*', check_type=Ban.USERNAME)
        details = {
            'username': 'Misago Admin',
            'full_name': u'Błob Błopo',
        }
        result = get_username(None, details, None)
        self.assertEqual(result, {'clean_username': 'BlobBlopo'})

    def test_resolve_to_cut_name(self):
        """pipeline will resolve cut too long name on second pass"""
        details = {
            'username': u'Abrakadabrapokuskonstantynopolitańczykowianeczkatrzy',
        }
        result = get_username(None, details, None)
        self.assertEqual(result, {'clean_username': 'Abrakadabrapok'})


class ValidateIpNotBannedTests(PipelineTestCase):
    def test_skip_if_user_not_set(self):
        """pipeline step is skipped if no user was passed"""
        result = validate_ip_not_banned(None, {}, GithubOAuth2)
        self.assertIsNone(result)

    def test_raise_if_banned(self):
        """pipeline raises if user's IP is banned"""
        Ban.objects.create(banned_value='188.*', check_type=Ban.IP)

        try:
            validate_ip_not_banned(MockStrategy(user_ip='188.1.2.3'), {}, GithubOAuth2, self.user)
            self.fail("validate_ip_not_banned should raise SocialAuthBanned")
        except SocialAuthBanned as e:
            self.assertTrue(isinstance(e.ban, Ban))

    def test_exclude_staff(self):
        """pipeline excludes staff from bans"""
        self.user.is_staff = True
        self.user.save()

        Ban.objects.create(banned_value='188.*', check_type=Ban.IP)

        result = validate_ip_not_banned(
            MockStrategy(user_ip='188.1.2.3'), {}, GithubOAuth2, self.user)
        self.assertIsNone(result)


class ValidateUserNotBannedTests(PipelineTestCase):
    def test_skip_if_user_not_set(self):
        """pipeline step is skipped if no user was passed"""
        result = validate_user_not_banned(None, {}, GithubOAuth2)
        self.assertIsNone(result)

    def test_raise_if_banned(self):
        """pipeline raises if user's IP is banned"""
        Ban.objects.create(banned_value=self.user.username, check_type=Ban.USERNAME)

        try:
            validate_user_not_banned(MockStrategy(), {}, GithubOAuth2, self.user)
            self.fail("validate_ip_not_banned should raise SocialAuthBanned")
        except SocialAuthBanned as e:
            self.assertEqual(e.ban.user, self.user)
            self.assertTrue(isinstance(e.ban, BanCache))

    def test_exclude_staff(self):
        """pipeline excludes staff from bans"""
        self.user.is_staff = True
        self.user.save()

        Ban.objects.create(banned_value=self.user.username, check_type=Ban.USERNAME)

        result = validate_user_not_banned(MockStrategy(), {}, GithubOAuth2, self.user)
        self.assertIsNone(result)
