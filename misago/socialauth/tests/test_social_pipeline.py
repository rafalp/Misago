import json
from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import RequestFactory
from social_core.backends.github import GithubOAuth2
from social_django.utils import load_strategy

from ...acl.useracl import get_user_acl
from ...conf.dynamicsettings import DynamicSettings
from ...conf.test import override_dynamic_settings
from ...conftest import get_cache_versions
from ...core.exceptions import SocialAuthBanned, SocialAuthFailed
from ...legal.models import Agreement
from ...users.models import AnonymousUser, Ban, BanCache
from ...users.test import UserTestCase
from ..pipeline import (
    associate_by_email,
    create_user,
    create_user_with_form,
    get_username,
    require_activation,
    validate_ip_not_banned,
    validate_user_not_banned,
)

User = get_user_model()


def create_request(user_ip="0.0.0.0", data=None):
    factory = RequestFactory()
    if data is None:
        request = factory.get("/")
    else:
        request = factory.post(
            "/", data=json.dumps(data), content_type="application/json"
        )
    request.include_frontend_context = True
    request.cache_versions = get_cache_versions()
    request.frontend_context = {}
    request.socialauth = {}
    request.session = {}
    request.settings = DynamicSettings(request.cache_versions)
    request.user = AnonymousUser()
    request.user_acl = get_user_acl(request.user, request.cache_versions)
    request.user_ip = user_ip
    return request


def create_strategy():
    request = create_request()
    return load_strategy(request=request)


class MockStrategy:
    def __init__(self, user_ip="0.0.0.0"):
        self.cleaned_partial_token = None
        self.request = create_request(user_ip)

    def clean_partial_pipeline(self, token):
        self.cleaned_partial_token = token


class PipelineTestCase(UserTestCase):
    def get_initial_user(self):
        self.user = self.get_authenticated_user()

    def assertNewUserIsCorrect(
        self, new_user, form_data=None, activation=None, email_verified=False
    ):
        self.assertFalse(new_user.has_usable_password())
        self.assertIn("Welcome", mail.outbox[0].subject)

        if form_data:
            self.assertEqual(new_user.email, form_data["email"])
            self.assertEqual(new_user.username, form_data["username"])

        if activation == "none":
            self.assertEqual(new_user.requires_activation, User.ACTIVATION_NONE)

        if activation == "user":
            if email_verified:
                self.assertEqual(new_user.requires_activation, User.ACTIVATION_NONE)
            else:
                self.assertEqual(new_user.requires_activation, User.ACTIVATION_USER)

        if activation == "admin":
            self.assertEqual(new_user.requires_activation, User.ACTIVATION_ADMIN)

        self.assertEqual(new_user.audittrail_set.count(), 1)

    def assertJsonResponseEquals(self, response, value):
        response_content = response.content.decode("utf-8")
        response_json = json.loads(response_content)
        self.assertEqual(response_json, value)


class AssociateByEmailTests(PipelineTestCase):
    def test_skip_if_user_is_already_set(self):
        """pipeline step is skipped if user was found by previous step"""
        result = associate_by_email(Mock(), {}, GithubOAuth2, self.user)
        self.assertIsNone(result)

    def test_skip_if_no_email_passed(self):
        """pipeline step is skipped if no email was passed"""
        result = associate_by_email(Mock(), {}, GithubOAuth2)
        self.assertIsNone(result)

    def test_skip_if_user_with_email_not_found(self):
        """pipeline step is skipped if no email was passed"""
        result = associate_by_email(Mock(), {"email": "not@found.com"}, GithubOAuth2)
        self.assertIsNone(result)

    def test_raise_if_user_is_inactive(self):
        """pipeline raises if user was inactive"""
        strategy = Mock(setting=Mock(return_value=True))
        self.user.is_active = False
        self.user.save()

        try:
            associate_by_email(strategy, {"email": self.user.email}, GithubOAuth2)
            self.fail("associate_by_email should raise SocialAuthFailed")
        except SocialAuthFailed as e:
            self.assertEqual(
                e.message,
                (
                    "The e-mail address associated with your GitHub account "
                    "is not available for use on this site."
                ),
            )

    def test_raise_if_user_needs_admin_activation(self):
        """pipeline raises if user needs admin activation"""
        strategy = Mock(setting=Mock(return_value=True))
        self.user.requires_activation = User.ACTIVATION_ADMIN
        self.user.save()

        try:
            associate_by_email(strategy, {"email": self.user.email}, GithubOAuth2)
            self.fail("associate_by_email should raise SocialAuthFailed")
        except SocialAuthFailed as e:
            self.assertEqual(
                e.message,
                (
                    "Your account has to be activated by site administrator "
                    "before you will be able to sign in with GitHub."
                ),
            )

    def test_no_user_is_returned_if_pipeline_is_disabled(self):
        strategy = Mock(setting=Mock(return_value=False))
        result = associate_by_email(strategy, {"email": self.user.email}, GithubOAuth2)
        self.assertIsNone(result)
        strategy.setting.assert_called_once_with(
            "ASSOCIATE_BY_EMAIL", default=False, backend=GithubOAuth2
        )

    def test_return_user(self):
        """pipeline returns user if email was found"""
        strategy = Mock(setting=Mock(return_value=True))
        result = associate_by_email(strategy, {"email": self.user.email}, GithubOAuth2)
        self.assertEqual(result, {"user": self.user, "is_new": False})

    def test_return_user_email_inactive(self):
        """pipeline returns user even if they didn't activate their account manually"""
        strategy = Mock(setting=Mock(return_value=True))
        self.user.requires_activation = User.ACTIVATION_USER
        self.user.save()

        result = associate_by_email(strategy, {"email": self.user.email}, GithubOAuth2)
        self.assertEqual(result, {"user": self.user, "is_new": False})


class CreateUser(PipelineTestCase):
    def test_skip_if_user_is_set(self):
        """pipeline step is skipped if user was passed"""
        result = create_user(MockStrategy(), {}, GithubOAuth2(), user=self.user)
        self.assertIsNone(result)

    def test_skip_if_no_email_passed(self):
        """pipeline step is skipped if no email was passed"""
        result = create_user(
            MockStrategy(), {}, GithubOAuth2(), clean_username="TestBob"
        )
        self.assertIsNone(result)

    def test_skip_if_no_clean_username_passed(self):
        """pipeline step is skipped if cleaned username wasnt passed"""
        result = create_user(
            MockStrategy(), {"email": "hello@example.com"}, GithubOAuth2()
        )
        self.assertIsNone(result)

    def test_skip_if_email_is_taken(self):
        """pipeline step is skipped if email was taken"""
        result = create_user(
            MockStrategy(),
            {"email": self.user.email},
            GithubOAuth2(),
            clean_username="NewUser",
        )
        self.assertIsNone(result)

    @override_dynamic_settings(account_activation="none")
    def test_user_created_no_activation(self):
        """pipeline step creates active user for valid data and disabled activation"""
        result = create_user(
            MockStrategy(),
            {"email": "new@example.com"},
            GithubOAuth2(),
            clean_username="NewUser",
        )
        new_user = User.objects.get(email="new@example.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})
        self.assertEqual(new_user.username, "NewUser")
        self.assertNewUserIsCorrect(new_user, email_verified=True, activation="none")

    @override_dynamic_settings(account_activation="user")
    def test_user_created_activation_by_user(self):
        """pipeline step creates active user for valid data and user activation"""
        result = create_user(
            MockStrategy(),
            {"email": "new@example.com"},
            GithubOAuth2(),
            clean_username="NewUser",
        )
        new_user = User.objects.get(email="new@example.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})
        self.assertEqual(new_user.username, "NewUser")
        self.assertNewUserIsCorrect(new_user, email_verified=True, activation="user")

    @override_dynamic_settings(account_activation="admin")
    def test_user_created_activation_by_admin(self):
        """pipeline step creates in user for valid data and admin activation"""
        result = create_user(
            MockStrategy(),
            {"email": "new@example.com"},
            GithubOAuth2(),
            clean_username="NewUser",
        )
        new_user = User.objects.get(email="new@example.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})
        self.assertEqual(new_user.username, "NewUser")
        self.assertNewUserIsCorrect(new_user, email_verified=True, activation="admin")


class CreateUserWithFormTests(PipelineTestCase):
    def setUp(self):
        super().setUp()

        Agreement.objects.invalidate_cache()

    def tearDown(self):
        super().tearDown()

        Agreement.objects.invalidate_cache()

    def test_skip_if_user_is_set(self):
        """pipeline step is skipped if user was passed"""
        request = create_request()
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={},
            backend=backend,
            user=self.user,
            pipeline_index=1,
        )
        self.assertEqual(result, {})

    def test_renders_form_if_not_post(self):
        """pipeline step renders form if not POST"""
        request = create_request()
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        response = create_user_with_form(
            strategy=strategy, details={}, backend=backend, user=None, pipeline_index=1
        )
        self.assertContains(response, "GitHub")

    def test_empty_data_rejected(self):
        """form rejects empty data"""
        request = create_request(data={})
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        response = create_user_with_form(
            strategy=strategy, details={}, backend=backend, user=None, pipeline_index=1
        )
        self.assertEqual(response.status_code, 400)
        self.assertJsonResponseEquals(
            response,
            {
                "email": ["This field is required."],
                "username": ["This field is required."],
            },
        )

    def test_taken_data_rejected(self):
        """form rejects taken data"""
        request = create_request(
            data={"email": self.user.email, "username": self.user.username}
        )
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        response = create_user_with_form(
            strategy=strategy, details={}, backend=backend, user=None, pipeline_index=1
        )
        self.assertEqual(response.status_code, 400)
        self.assertJsonResponseEquals(
            response,
            {
                "email": ["This e-mail address is not available."],
                "username": ["This username is not available."],
            },
        )

    @override_dynamic_settings(account_activation="none")
    def test_user_created_no_activation_verified_email(self):
        """active user is created for verified email and activation disabled"""
        form_data = {"email": "social@auth.com", "username": "SocialUser"}
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={"email": form_data["email"]},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertNewUserIsCorrect(
            new_user, form_data, activation="none", email_verified=True
        )

    @override_dynamic_settings(account_activation="none")
    def test_user_created_no_activation_nonverified_email(self):
        """active user is created for non-verified email and activation disabled"""
        form_data = {"email": "social@auth.com", "username": "SocialUser"}
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={"email": ""},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertNewUserIsCorrect(
            new_user, form_data, activation="none", email_verified=False
        )

    @override_dynamic_settings(account_activation="user")
    def test_user_created_activation_by_user_verified_email(self):
        """active user is created for verified email and activation by user"""
        form_data = {"email": "social@auth.com", "username": "SocialUser"}
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={"email": form_data["email"]},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertNewUserIsCorrect(
            new_user, form_data, activation="user", email_verified=True
        )

    @override_dynamic_settings(account_activation="user")
    def test_user_created_activation_by_user_nonverified_email(self):
        """inactive user is created for non-verified email and activation by user"""
        form_data = {"email": "social@auth.com", "username": "SocialUser"}
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={"email": ""},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertNewUserIsCorrect(
            new_user, form_data, activation="user", email_verified=False
        )

    @override_dynamic_settings(account_activation="admin")
    def test_user_created_activation_by_admin_verified_email(self):
        """inactive user is created for verified email and activation by admin"""
        form_data = {"email": "social@auth.com", "username": "SocialUser"}
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={"email": form_data["email"]},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertNewUserIsCorrect(
            new_user, form_data, activation="admin", email_verified=True
        )

    @override_dynamic_settings(account_activation="admin")
    def test_user_created_activation_by_admin_nonverified_email(self):
        """inactive user is created for non-verified email and activation by admin"""
        form_data = {"email": "social@auth.com", "username": "SocialUser"}
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={"email": ""},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertNewUserIsCorrect(
            new_user, form_data, activation="admin", email_verified=False
        )

    def test_form_check_agreement(self):
        """social register checks agreement"""
        form_data = {"email": "social@auth.com", "username": "SocialUser"}
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS, text="Lorem ipsum", is_active=True
        )

        response = create_user_with_form(
            strategy=strategy,
            details={"email": form_data["email"]},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJsonResponseEquals(
            response, {"terms_of_service": ["This agreement is required."]}
        )

        # invalid agreement id
        form_data = {
            "email": "social@auth.com",
            "username": "SocialUser",
            "terms_of_service": agreement.id + 1,
        }
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        response = create_user_with_form(
            strategy=strategy,
            details={"email": form_data["email"]},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJsonResponseEquals(
            response, {"terms_of_service": ["This agreement is required."]}
        )

        # valid agreement id
        form_data = {
            "email": "social@auth.com",
            "username": "SocialUser",
            "terms_of_service": agreement.id,
        }
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = create_user_with_form(
            strategy=strategy,
            details={"email": form_data["email"]},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertEqual(new_user.agreements, [agreement.id])
        self.assertEqual(new_user.useragreement_set.count(), 1)

    def test_form_ignore_inactive_agreement(self):
        """social register ignores inactive agreement"""
        form_data = {
            "email": "social@auth.com",
            "username": "SocialUser",
            "terms_of_service": None,
        }
        request = create_request(data=form_data)
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        Agreement.objects.create(
            type=Agreement.TYPE_TOS, text="Lorem ipsum", is_active=False
        )

        result = create_user_with_form(
            strategy=strategy,
            details={"email": form_data["email"]},
            backend=backend,
            user=None,
            pipeline_index=1,
        )

        new_user = User.objects.get(email="social@auth.com")
        self.assertEqual(result, {"user": new_user, "is_new": True})

        self.assertEqual(new_user.agreements, [])
        self.assertEqual(new_user.useragreement_set.count(), 0)


class GetUsernameTests(PipelineTestCase):
    def test_skip_if_user_is_set(self):
        """pipeline step is skipped if user was passed"""
        strategy = create_strategy()
        result = get_username(strategy, {}, None, user=self.user)
        self.assertIsNone(result)

    def test_skip_if_no_names(self):
        """pipeline step is skipped if API returned no names"""
        strategy = create_strategy()
        result = get_username(strategy, {}, None)
        self.assertIsNone(result)

    def test_resolve_to_username(self):
        """pipeline step resolves username"""
        strategy = create_strategy()
        result = get_username(strategy, {"username": "BobBoberson"}, None)
        self.assertEqual(result, {"clean_username": "BobBoberson"})

    def test_normalize_username(self):
        """pipeline step normalizes username"""
        strategy = create_strategy()
        result = get_username(strategy, {"username": "Błop Błoperson"}, None)
        self.assertEqual(result, {"clean_username": "BlopBloperson"})

    def test_resolve_to_first_name(self):
        """pipeline attempts to use first name because username is taken"""
        strategy = create_strategy()
        details = {"username": self.user.username, "first_name": "Błob"}
        result = get_username(strategy, details, None)
        self.assertEqual(result, {"clean_username": "Blob"})

    def test_dont_resolve_to_last_name(self):
        """pipeline will not fallback to last name because username is taken"""
        strategy = create_strategy()
        details = {"username": self.user.username, "last_name": "Błob"}
        result = get_username(strategy, details, None)
        self.assertIsNone(result)

    def test_resolve_to_first_last_name_first_char(self):
        """pipeline will construct username from first name and first char of surname"""
        strategy = create_strategy()
        details = {"first_name": self.user.username, "last_name": "Błob"}
        result = get_username(strategy, details, None)
        self.assertEqual(result, {"clean_username": self.user.username + "B"})

    def test_dont_resolve_to_banned_name(self):
        """pipeline will not resolve to banned name"""
        strategy = create_strategy()
        Ban.objects.create(banned_value="*Admin*", check_type=Ban.USERNAME)
        details = {"username": "Misago Admin", "first_name": "Błob"}
        result = get_username(strategy, details, None)
        self.assertEqual(result, {"clean_username": "Blob"})

    def test_resolve_full_name(self):
        """pipeline will resolve to full name"""
        strategy = create_strategy()
        Ban.objects.create(banned_value="*Admin*", check_type=Ban.USERNAME)
        details = {"username": "Misago Admin", "full_name": "Błob Błopo"}
        result = get_username(strategy, details, None)
        self.assertEqual(result, {"clean_username": "BlobBlopo"})

    def test_resolve_to_cut_name(self):
        """pipeline will resolve cut too long name on second pass"""
        strategy = create_strategy()
        details = {"username": "Abrakadabrapokuskonstantynopolitańczykowianeczkatrzy"}
        result = get_username(strategy, details, None)
        self.assertEqual(result, {"clean_username": "Abrakadabrapok"})


class RequireActivationTests(PipelineTestCase):
    def setUp(self):
        super().setUp()

        self.user.requires_activation = User.ACTIVATION_ADMIN
        self.user.save()

    def test_skip_if_user_not_set(self):
        """pipeline step is skipped if user is not set"""
        request = create_request()
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = require_activation(
            strategy=strategy, details={}, backend=backend, user=None, pipeline_index=1
        )
        self.assertEqual(result, {})

    def test_partial_token_if_user_not_set_no_showstopper(self):
        """pipeline step handles set session token if user is not set"""
        request = create_request()
        strategy = load_strategy(request=request)
        strategy.request.session["partial_pipeline_token"] = "test-token"
        backend = GithubOAuth2(strategy, "/")

        require_activation(
            strategy=strategy, details={}, backend=backend, user=None, pipeline_index=1
        )

    def test_skip_if_user_is_active(self):
        """pipeline step is skipped if user is active"""
        self.user.requires_activation = User.ACTIVATION_NONE
        self.user.save()

        self.assertFalse(self.user.requires_activation)

        request = create_request()
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        result = require_activation(
            strategy=strategy,
            details={},
            backend=backend,
            user=self.user,
            pipeline_index=1,
        )
        self.assertEqual(result, {})

    def test_pipeline_returns_html_response_on_get(self):
        """pipeline step renders http response for GET request and inactive user"""
        request = create_request()
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        response = require_activation(
            strategy=strategy,
            details={},
            backend=backend,
            user=self.user,
            pipeline_index=1,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "text/html; charset=utf-8")

    def test_pipeline_returns_json_response_on_post(self):
        """pipeline step renders json response for POST request and inactive user"""
        request = create_request(data={"username": "anything"})
        strategy = load_strategy(request=request)
        backend = GithubOAuth2(strategy, "/")

        response = require_activation(
            strategy=strategy,
            details={},
            backend=backend,
            user=self.user,
            pipeline_index=1,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        self.assertJsonResponseEquals(
            response,
            {
                "step": "done",
                "backend_name": "GitHub",
                "activation": "admin",
                "email": "test@user.com",
                "username": "TestUser",
            },
        )


class ValidateIpNotBannedTests(PipelineTestCase):
    def test_skip_if_user_not_set(self):
        """pipeline step is skipped if no user was passed"""
        result = validate_ip_not_banned(None, {}, GithubOAuth2)
        self.assertIsNone(result)

    def test_raise_if_banned(self):
        """pipeline raises if user's IP is banned"""
        Ban.objects.create(banned_value="188.*", check_type=Ban.IP)

        try:
            validate_ip_not_banned(
                MockStrategy(user_ip="188.1.2.3"), {}, GithubOAuth2, self.user
            )
            self.fail("validate_ip_not_banned should raise SocialAuthBanned")
        except SocialAuthBanned as e:
            self.assertTrue(isinstance(e.ban, Ban))

    def test_exclude_staff(self):
        """pipeline excludes staff from bans"""
        self.user.is_staff = True
        self.user.save()

        Ban.objects.create(banned_value="188.*", check_type=Ban.IP)

        result = validate_ip_not_banned(
            MockStrategy(user_ip="188.1.2.3"), {}, GithubOAuth2, self.user
        )
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
